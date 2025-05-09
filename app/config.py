import yaml
import os
from dataclasses import dataclass, asdict, field
from typing import List, Dict
from lingua import Language
from .audio.utils import get_default_output_name
from .logger import get_logger

logger = get_logger("Config")

@dataclass
class Config:
  output_device: str
  stt_model: str = 'small'
  enable_tts: bool = True
  enable_osc: bool = True
  tts_models: Dict[str, str] = field(
    default_factory=lambda: {
      "ENGLISH": "en-US-AriaNeural",
      "JAPANESE": "ja-JP-NanamiNeural",
      "CHINESE": "zh-CN-XiaoxiaoNeural"
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
    try:
      with open(path, 'r') as f:
        data = yaml.safe_load(f)
        
      obj = cls(**data)
      obj.validate()
      return obj
    except Exception as e:
      logger.warning(f"Invalid config file: {e}")
      return cls.new(path)
      
  @classmethod
  def new(cls, path: str):
    try:
      old_config_path = f"{path}.old"
      os.rename(path, old_config_path)
    except FileNotFoundError:
      pass
    except Exception as e:
      logger.warning("Unable to rename old config file.")
      
    obj = cls(get_default_output_name())
    obj.save(path)
    return obj
  
  def save(self, path: str):
    with open(path, 'w') as f:
      yaml.safe_dump(asdict(self), f)
