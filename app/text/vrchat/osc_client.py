from pythonosc.udp_client import SimpleUDPClient

class OSCClient:
  def __init__(self):
    self.client = SimpleUDPClient("127.0.0.1", 9000)
    
  def process_text(self, text):
    self.client.send_message("/chatbox/input", [text, True])