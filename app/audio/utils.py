import sounddevice as sd

def get_default_output_name():
  default_output_idx = sd.default.device[1]
  default_output = sd.query_devices(default_output_idx)
  
  return default_output['name']