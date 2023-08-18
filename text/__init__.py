""" from https://github.com/keithito/tacotron """
from text import cleaners
from text.symbols import symbols
from phonemizer.backend import EspeakBackend

backend_vn = EspeakBackend(language = 'vi', 
                           preserve_punctuation=True, 
                           with_stress=True, 
                           language_switch='remove-flags')

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def text_to_sequence(text, cleaner_names):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []
  if cleaner_names != 'vietnamese_cleaners': clean_text = _clean_text(text, cleaner_names, backend_vn)
  else:  clean_text = _clean_text(text, cleaner_names)
  for symbol in clean_text:
    symbol_id = _symbol_to_id[symbol]
    sequence += [symbol_id]
  return sequence


def cleaned_text_to_sequence(cleaned_text):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
  return sequence


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    s = _id_to_symbol[symbol_id]
    result += s
  return result


def _clean_text(text, cleaner_names, backend=None):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    if name != 'vietnamese_cleaners':
      text = cleaner(text)
    else:
      text = cleaner(text, backend)
  return text
