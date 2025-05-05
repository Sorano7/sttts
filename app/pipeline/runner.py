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
    
  def load_config(self):
    pass
  
  async def start(self):
    pass

