from app.main import main
from app.logger import set_global_log_level, set_global_log_format

set_global_log_level("INFO")
set_global_log_format("time(%H:%M:%S) | level | msg")

if __name__ == '__main__':
  main()