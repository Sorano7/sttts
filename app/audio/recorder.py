import numpy as np
import webrtcvad
import collections
import sounddevice as sd
import queue
import asyncio
from ..logger import get_logger

logger = get_logger("AudioRecorder")

class AudioRecorder:
  def __init__(
    self,
    output_queue: asyncio.Queue,
    silence_threshold_sec=1.0,
    channels=1,
    rate=16000,
    chunk_duration_ms=30,
    vad_aggressiveness=3
  ):
    assert chunk_duration_ms in [10, 20, 30], "Chunk duration must be 10, 20, or 30 ms."
    
    self.silence_threshold_sec = silence_threshold_sec
    self.channels = channels
    self.rate = rate
    self.chunk_duration_ms = chunk_duration_ms
    self.vad = webrtcvad.Vad(vad_aggressiveness)
    
    self.chunk_size = int(rate * chunk_duration_ms / 1000)
    self.ring_buffer_size = int(silence_threshold_sec * 1000 / chunk_duration_ms)
    self.ring_buffer = collections.deque(maxlen=self.ring_buffer_size)
    
    self.recording = False
    self.voiced_frames = []
    self.running = True
    
    self.audio_queue = queue.Queue()
    self.output_queue = output_queue
    
    self.stop_event = asyncio.Event()
    
  def is_speech(self, data):
    try:
      return self.vad.is_speech(data, self.rate)
    except Exception as e:
      logger.error(f"VAD error: {e}")
      return False
    
  def callback(self, indata, frames, time, status):
    audio_int16 = (indata * 32767).astype(np.int16)
    audio_bytes = audio_int16.tobytes()

    self.audio_queue.put(audio_bytes)

    
  async def process_audio(self):
    while not self.stop_event.is_set():
      try:
        while not self.audio_queue.empty():
          data = self.audio_queue.get_nowait()
          await self.process_audio_chunk(data)       
          self.audio_queue.task_done()
          
        await asyncio.sleep(0.001)
      except queue.Empty:
        pass
      except asyncio.CancelledError:
        break
      except Exception as e:
        logger.error(f"Failed to process audio: {e}")
        
  async def process_audio_chunk(self, data):
    is_speech = self.is_speech(data)
    self.ring_buffer.append(is_speech)
    
    if not self.recording:
      if is_speech:
        self.recording = True
        self.voiced_frames.append(data)
        
    else:
      self.voiced_frames.append(data)
      
      if len(self.ring_buffer) >= self.ring_buffer_size:
        num_unvoiced = len([v for v in self.ring_buffer if not v])
        if num_unvoiced == self.ring_buffer_size:
          recording_data = b''.join(self.voiced_frames)
          await self.output_queue.put(recording_data)
          logger.debug("Silence detected. Segment pushed to output.")
          
          self.voiced_frames = []
          self.recording = False
          self.ring_buffer.clear()
        
  async def start(self):
    logger.info("Running.")
    
    process_task = asyncio.create_task(self.process_audio())
    
    stream = sd.InputStream(
      samplerate=self.rate,
      channels=self.channels,
      callback=self.callback,
      blocksize=self.chunk_size,
      dtype='float32'
    )
    
    try:
      with stream:
        await self.stop_event.wait()
    finally:
      process_task.cancel()
      try:
        await process_task
      except asyncio.CancelledError:
        pass
      
  async def stop(self):
    logger.info("Stopped.")
    self.stop_event.set()