import os
import asyncio
from .pipeline.runner import Runner
from .config import Config
from .audio.utils import get_default_output_name

class STTTS:
  CONFIG_PATH = "./config.yaml"
  
  def __init__(self):
    self.load_config()
    self.runner = Runner(self.config)
  
  def load_config(self):
    try:
      config = Config.load(self.CONFIG_PATH)
      self.config = config
    except Exception as e:
      print(f"[STTTS] Invalid config file: {e}. Generating new config file...")
      try:
        os.rename(self.CONFIG_PATH, f"{self.CONFIG_PATH}.old")
      except:
        pass
      self._generate_new_config()
      
  def _generate_new_config(self):
    try:
      old_config_path = f"{self.CONFIG_PATH}.old"
      os.rename(self.CONFIG_PATH, old_config_path)
    except FileNotFoundError:
      pass
    except Exception as e:
      print("[STTTS] Failed to rename old config file. Removing...")
    device = get_default_output_name()
    self.config = Config(output_device=device)
    self.config.save(self.CONFIG_PATH)
  
  def run_gui(self):
    pass
    
  def run(self):
    print("[STTTS] Starting...")
    try:
      asyncio.run(self.runner.run())
    except KeyboardInterrupt:
      print("[STTTS] Exited.")
  
  
if __name__ == "__main__":
  sttts = STTTS()
  sttts.run()