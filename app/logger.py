from datetime import datetime
from enum import Enum
from inspect import currentframe

class LogLevel(Enum):
  DEBUG = 10
  INFO = 20
  WARNING = 30
  ERROR = 40
  CRITICAL = 50
  
def _get_level(level: str):
  level = LogLevel.__members__.get(level)
  return level.value if level is not None else 0
  
class LogRunner:
  """Wrapper class to handle logging and global settings"""
  
  def __init__(self, level):
    self.level = _get_level(level)
  
  def should_print(self, level):
    return _get_level(level) >= self.level
  
  def set_level(self, level):
    self.level = _get_level(level)

class Logger:
  """Class for logging messages"""
  
  def __init__(self, runner: LogRunner, name="Main", level=None):
    self.runner = runner
    self.name = name
    self.level = None if level is None else _get_level(level)
    
  def _log(self, level, msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output = f"[{timestamp}] [{level}] [{self.name}] {msg}"
    
    if self.level is not None and _get_level(level) >= self.level:
      print(output)
    else:
      if self.runner.should_print(level):
        print(output)
    
  def debug(self, msg):
    self._log("DEBUG", msg)
    
  def info(self, msg):
    self._log("INFO", msg)
    
  def warning(self, msg):
    self._log("WARNING", msg)
    
  def error(self, msg):
    self._log("ERROR", msg)
    
  def critical(self, msg):
    self._log("CRITICAL", msg)
    
runner = LogRunner("INFO")

def set_global_log_level(level):
  """Set the global log level"""
  
  runner.set_level(level)
    
def get_logger(name="Main", level=None):
  """Get a logger object under the global LogRunner"""
  
  return Logger(runner, name, level)
    
def get_linenumber():
  cf = currentframe()
  return cf.f_back.f_lineno
  