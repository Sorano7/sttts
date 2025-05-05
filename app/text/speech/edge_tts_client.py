import asyncio
import os
import edge_tts
import tempfile
from pygame import mixer
from typing import Dict
from .utils import detect_language

class EdgeTTSClient:
  def __init__(
    self, 
    text_queue: asyncio.Queue, 
    models: Dict[str, str] = {
      "ENGLISH": "en-US-AnaNeural",
      "JAPANESE": "ja-JP-NanamiNeural",
      "CHINESE": "zh-CN-XiaoyiNeural"
    },
    output_device="VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO)"
  ):
    self.text_queue = text_queue
    self.output_device = output_device
    self.models = models
    
    self.stop_event = asyncio.Event()
    
  async def start(self):
    print("[Speech] Running.")
    
    while not self.stop_event.is_set():
      try:
        text = await self.text_queue.get()
        await self.process_text(text)
        self.text_queue.task_done()
        
      except asyncio.CancelledError:
        break
      except Exception as e:
        print("[Speech] Error:", e)
        
  async def process_text(self, text):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
      temp_filename = temp_audio.name
      
    model = self.model_to_use(text)
    if model is None:
      return
    
    client = edge_tts.Communicate(text, voice=model)
    await client.save(temp_filename)
    
    mixer.init(devicename=self.output_device)
    mixer.music.load(temp_filename)
    mixer.music.play()
    
    while mixer.music.get_busy():
      await asyncio.sleep(0.1)
      
    mixer.quit()
    os.remove(temp_filename)
      
  def model_to_use(self, text):
    language = detect_language(text)
    if language not in self.models.keys():
      return None
    return self.models[language]
  
  async def stop(self):
    print("[Speech] Stopped.")
    self.stop_event.set()
    