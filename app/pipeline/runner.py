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
    
    self.audio_recorder = AudioRecorder(
      output_queue=self.audio_queue
    )
    self.transcriber = WhisperClient(
      audio_queue=self.audio_queue, 
      text_queue=self.text_queue, 
      model_size=self.config.stt_model
    )
    self.text_processor = TextProcessor(
      queue=self.text_queue,
      config=self.config
    )
    
  async def run(self):
    tasks = [
      asyncio.create_task(self.audio_recorder.start()),
      asyncio.create_task(self.transcriber.start()),
      asyncio.create_task(self.text_processor.start())
    ]

    try:
      await asyncio.gather(*tasks)
    finally:
      await self.audio_recorder.stop()
      await self.transcriber.stop()
      await self.text_processor.stop()
      
      for task in tasks:
        task.cancel()
      await asyncio.gather(*task, return_exceptions=True)