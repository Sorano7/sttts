from app.main import main
from app.logger import set_global_log_level

set_global_log_level("INFO")

if __name__ == '__main__':
  main()