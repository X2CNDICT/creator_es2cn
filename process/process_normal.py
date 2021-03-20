import json

pos = ['n.pr.', 'm.pr.', 'm.pl.', 'f.pl.', 'm.f.', 'm.', 'f.', 'vi.', 'vt.', 'vr.', 'adj.', 'adv.', 'interj.', 'pron.', 'conj.', 'prep.', 'pl.', 'amb.', 'art.', 'impers.']

def get_json_content(filename):
  content = []
  with open(filename, 'r') as f:
    content = json.load(f)
  return content
 
def stack(meaning):
  seq = []
  e = []
  for index, s in enumerate(meaning):
    if len(e) != 0 and e[-1] not in pos and s in pos:
      seq.append(e)
      e = []
    e.append(s)
    if index == len(meaning) - 1:
      seq.append(e)
  return seq 

def es2cn(filename):
  content = get_json_content(filename)
  dictionary = []
  for e in content:
    dictionary.append({
      "word": e["pronounciation"],
      "explanation": stack(e['meaning'])
    })
  return dictionary
    

def distinct_keys(dictionary):
  _keys = []
  _dictionary = []
  for e in dictionary:
    if e["word"] not in _keys:
      _dictionary.append(e) 
  return _dictionary 


def to_dict(explanation):
  _semantic = {}
  for e in explanation[:-1]:  
    _semantic["pos"] = e
    _semantic["meaning"] = explanation[-1]
  return _semantic

def reform_explanation(d):
  _d = [] 
  for w in d:
    exs = w["explanation"] 
    reformed = []
    for e in exs:
      reformed.append(to_dict(e))
    _d.append({"word": w["word"], "explanation": reformed})
  return _d

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)
 
dictionary = es2cn('./src/spanish-chinese.json')

distinct_dict = distinct_keys(dictionary)

writeTo('./dst/spanish-chinese.json', reform_explanation(distinct_dict))
