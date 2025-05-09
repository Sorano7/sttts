import asyncio
import os
import edge_tts
import tempfile
from pygame import mixer
from typing import Dict
from .utils import to_language, detect_language

class EdgeTTSClient:
  def __init__(
    self, 
    output_device: str,
    models: Dict[str, str]
  ):
    self.models = models
    self.output_device = output_device
        
  async def process_text(self, text):
    try:
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
    except Exception as e:
      print("[EdgeTTSClient] Error:", e)
      
  def model_to_use(self, text):
    languages_to_detect = to_language(list(self.models.keys()))
    language = detect_language(text, languages_to_detect)
    if language not in self.models.keys():
      return None
    return self.models[language]
    