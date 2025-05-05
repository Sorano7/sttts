import asyncio
from .speech.edge_tts_client import EdgeTTSClient
from .vrchat.osc_client import OSCClient

class TextProcessor:
  def __init__(
    self,
    queue: asyncio.Queue,
    send_to_tts = True,
    send_to_osc = True
  ):
    self.queue = queue
    self.tts_client = None
    self.osc_client = None
    
    if send_to_tts:
      self.tts_client = EdgeTTSClient(self.queue)
      self.osc_client = OSCClient()
      
    self.stop_event = asyncio.Event()