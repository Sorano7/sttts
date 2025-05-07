import yaml
from dataclasses import dataclass, asdict, field
from typing import List, Dict
from lingua import Language

@dataclass
class Config:
  output_device: str
  stt_model: str = 'small'
  enable_tts: bool = True
  enable_osc: bool = True
  tts_models: Dict[str, str] = field(
    default_factory=lambda: {
      "ENGLISH": "en-US-AnaNeural",
      "JAPANESE": "ja-JP-NanamiNeural",
      "CHINESE": "zh-CN-XiaoyiNeural"
    }
  )

  def language_to_detect(self):
    return list(self.tts_models.keys())
  
  def validate(self):
    for lang in self.language_to_detect():
      if not Language.from_str(lang):
        raise ValueError('Invalid language')
  
  @classmethod
  def load(cls, path: str):
    with open(path, 'r') as f:
      data = yaml.safe_load(f)
      
    obj = cls(**data)
    obj.validate()
    return obj
    
  def save(self, path: str):
    with open(path, 'w') as f:
      yaml.safe_dump(asdict(self), f)
