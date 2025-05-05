import asyncio
from .speech.edge_tts_client import EdgeTTSClient
from .vrchat.osc_client import OSCClient

class TextProcessor:
  def __init__(
    self,
    queue: asyncio.Queue,
    tts_output_device,
    send_to_tts = True,
    send_to_osc = True,
  ):
    self.queue = queue
    self.tts_client = EdgeTTSClient(tts_output_device) if send_to_tts else None
    self.osc_client = OSCClient() if send_to_osc else None
      
    self.stop_event = asyncio.Event()
    
  async def start(self):
    print("[TextProcessor] Running.")
    
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
        print("[TextProcessor] Error:", e)
        
  async def process_text(self, text):
    print(f"[Output] {text}")
    
    if self.tts_client:
      await self.tts_client.process_text(text)
    if self.osc_client:
      self.osc_client.process_text(text)
      
  async def stop(self):
    print("[TextProcessor] Stopped.")
    self.stop_event.set()