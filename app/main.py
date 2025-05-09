import os
import sys
import asyncio
from .pipeline.runner import Runner
from .config import Config


class STTTS:
  def __init__(self):
    self.config_path = self._get_config_path()
    self.config = Config.load(self.config_path)
    self.runner = Runner(self.config)
  
  def _get_config_path(self):
    exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
    exe_dir = os.path.dirname(os.path.abspath(exe_path))
    return os.path.join(exe_dir, "config.yml")

  def run(self):
    print("[STTTS] Starting...")
    try:
      asyncio.run(self.runner.run())
    except KeyboardInterrupt:
      print("[STTTS] Exited.")
  
def main():
  sttts = STTTS()
  sttts.run()
  
if __name__ == "__main__":
  main()