from pythonosc.udp_client import SimpleUDPClient
from ...logger import get_logger

logger = get_logger("OSC")

class OSCClient:
  def __init__(self):
    self.client = SimpleUDPClient("127.0.0.1", 9000)
    
  def process_text(self, text):
    try:
      self.client.send_message("/chatbox/input", [text, True])
    except Exception as e:
      logger.error(f"{e}. Is VRChat running?")