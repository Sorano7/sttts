import sys
import os
from pathlib import Path

def set_cuda_paths():
  venv_base = Path(sys.executable).parent.parent
  nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
  cuda_path = nvidia_base_path / 'cuda_runtime' / 'bin'
  cublas_path = nvidia_base_path / 'cublas' / 'bin'
  cudnn_path = nvidia_base_path / 'cudnn' / 'bin'
  paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]
  env_vars = ['CUDA_PATH', 'CUDA_PATH_V12_4', 'PATH']
  
  for env_var in env_vars:
    current_value = os.environ.get(env_var, '')
    new_value = os.pathsep.join(paths_to_add + [current_value] if current_value else paths_to_add)
    os.environ[env_var] = new_value

set_cuda_paths()

import asyncio
import numpy as np
from faster_whisper import WhisperModel
from ..logger import get_logger

logger = get_logger("Transcriber")

class WhisperClient:
  def __init__(self, audio_queue: asyncio.Queue, text_queue: asyncio.Queue, model_size='base'):
    self.audio_queue = audio_queue
    self.text_queue = text_queue
    self.model = WhisperModel(model_size, compute_type="float16")
    
    self.stop_event = asyncio.Event()
    
  async def start(self):
    logger.info("Running.")
    while not self.stop_event.is_set():
      try:
        data = await self.audio_queue.get()
        text = self.transcribe_audio(data)
        if text is not None and text.strip():
          await self.text_queue.put(text)
          logger.info("Speech transcribed.")

        self.audio_queue.task_done()
      except asyncio.CancelledError:
        break
      except Exception as e:
        logger.error(f"{e}")
        
        
  def transcribe_audio(self, data):
    audio_array = np.frombuffer(data, dtype=np.int16)
    audio_float = audio_array.astype(np.float32) / 32767.0
    
    try:
      segments, _ = self.model.transcribe(audio_float, vad_filter=True, beam_size=3)
      return " ".join(segment.text for segment in segments)
    except Exception as e:
      logger.error(f"Transcription failed: {e}")
      return None
  
  async def stop(self):
    logger.info("Stopped.")
    self.stop_event.set()