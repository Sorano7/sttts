import asyncio
from ..config import Config
from .speech.edge_tts_client import EdgeTTSClient
from .vrchat.osc_client import OSCClient
from ..logger import get_logger

logger = get_logger("TextProcessor")

class TextProcessor:
  def __init__(
    self,
    queue: asyncio.Queue,
    config: Config
  ):
    self.queue = queue
    self.tts_client = EdgeTTSClient(
      output_device=config.output_device, 
      models=config.tts_models
    ) if config.enable_tts else None
    self.osc_client = OSCClient()  if config.enable_osc else None
      
    self.stop_event = asyncio.Event()
    
  async def start(self):
    logger.debug("Running.")
    
    while not self.stop_event.is_set():
      try:
        text = await self.queue.get()
        text = text.strip()
        if text:
          await self.process_text(text)
        self.queue.task_done()
      
      except asyncio.CancelledError:
        break
      
      except Exception as e:
        logger.error(f"{e}")
        
  async def process_text(self, text):
    logger.info(f"Output -> {text}")
    
    if self.tts_client:
      await self.tts_client.process_text(text)
    if self.osc_client:
      self.osc_client.process_text(text)
      
  async def stop(self):
    logger.debug("Stopped.")
    self.stop_event.set()