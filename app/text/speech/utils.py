from typing import List
from lingua import Language, LanguageDetectorBuilder

DEFAULT_LANGS = [Language.ENGLISH, Language.JAPANESE, Language.CHINESE]

def detect_language(text, languages: List[Language]):
  if not languages:
    return None

  detector = LanguageDetectorBuilder.from_languages(*languages).with_low_accuracy_mode().build()
  
  detected = []
  for result in detector.detect_multiple_languages_of(text):
    detected.append(result.language.name)
  
  if len(detected) > 1:
    return "ENGLISH"
  else:
    return detected[0]
  
  