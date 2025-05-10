import os
import sys
import asyncio
from .pipeline.runner import Runner
from .config import Config
from pathlib import Path
from .logger import get_logger, set_global_log_format, set_global_log_level

logger = get_logger("STTTS")

class STTTS:
  def __init__(self):
    self.config_path = self._get_config_path()
    self.config = Config.load(self.config_path)
    self.runner = Runner(self.config)
  
  def _get_config_path(self):
    if getattr(sys, 'frozen', False):
      base_path = Path(os.path.abspath(sys.executable)).parent
    else:
      base_path = Path(__file__).resolve().parent.parent
      
    return os.path.join(base_path, "config.yml")

  def run(self):
    logger.info("Started.")
    try:
      asyncio.run(self.runner.run())
    except KeyboardInterrupt:
      logger.info("Exited.")
  
def main():
  sttts = STTTS()
  sttts.run()
  
if __name__ == "__main__":
  set_global_log_level("DEBUG")
  set_global_log_format("time(%H:%M:%S) | level | file:line | name:: msg")
  main()