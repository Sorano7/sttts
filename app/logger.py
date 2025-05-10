from datetime import datetime
from enum import Enum
from pathlib import Path
from inspect import currentframe
import re

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
    self.set_level(level)
    self.format = "[time(%H:%M)] [level] [file] [name] msg"
  
  def should_print(self, level):
    return _get_level(level) >= self.level
  
  def set_level(self, level):
    self.level = _get_level(level)
    
  def set_format(self, format: str):
    self.format = format
      
  def format_log(self, level, msg, time, name, file, line):
    def replace(match):
      token = match.group(1)
      if token.startswith('time(') and token.endswith(')'):
        fmt = token[5:-1]
        return time.strftime(fmt)
      elif token == 'level':
        return level
      elif token == 'file':
        return f"{file}:{line}"
      elif token == 'name':
        return name
      elif token == 'msg':
        return msg
      
    return re.sub(r'(time\([^\)]+\)|level|file|name|msg)', replace, self.format)

class Logger:
  """Class for logging messages"""
  
  def __init__(self, runner: LogRunner, name="Main", level=None):
    self.runner = runner
    self.name = name
    self.level = None if level is None else _get_level(level)
    
  def _log(self, level, msg):
    timestamp = datetime.now()
    frame = currentframe().f_back.f_back
    filename = frame.f_code.co_filename
    filename = Path(filename).name
    lineno = frame.f_lineno
    output = self.runner.format_log(level, msg, timestamp, self.name, filename, lineno)
    
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
    
runner = LogRunner("DEBUG")

def set_global_log_level(level):
  """Set the global log level"""
  
  runner.set_level(level)
  
def set_global_log_format(format: str):
  """Set the global log format.
  
  Examples:
    - [time(%Y-%m-%d %H:%M)] [level] [file] msg
    - time(%H:%M:%S) | level | name: "msg"
  """
  runner.set_format(format)
    
def get_logger(name="Main", level=None):
  """Get a logger object under the global LogRunner"""
  
  return Logger(runner, name, level)