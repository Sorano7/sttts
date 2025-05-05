import asyncio

from ..config import Config
from ..audio.recorder import AudioRecorder
from ..transcriber.whisper_client import WhisperClient
from ..text.text_processor import TextProcessor

class Runner:
  def __init__(
    self,
    config: Config,
  ):
    self.config = config
    
    self.audio_queue = asyncio.Queue()
    self.text_queue = asyncio.Queue()
    
    self.audio_recorder = AudioRecorder(self.audio_queue)
    self.transcriber = WhisperClient(self.audio_queue, self.text_queue, self.config.stt_model)
    self.text_processor = TextProcessor(self.text_queue, self.config.enable_tts, self.config.enable_osc)
    
  async def run(self):
    record_task = asyncio.create_task(self.audio_recorder.start())
    transcribe_task = asyncio.create_task(self.transcriber.start())
    text_task = asyncio.create_task(self.text_processor.start())
    
    try:
      while True:
        await asyncio.sleep(0.1)
    finally:
      await self.audio_recorder.stop()
      await self.transcriber.stop()
      await self.text_processor.stop()
      
      await asyncio.gather(
        record_task,
        transcribe_task,
        text_task,
      )