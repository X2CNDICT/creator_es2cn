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

def mapped_tonics(letter):
  tonics = {
    'a': 'á',
    'e': 'é',
    'i': 'í',
    'o': 'ó'
  }
  if letter in tonics.keys():
    return tonics[letter]
  else:
    return letter

def es2cn(filename):
  content = get_json_content(filename)
  dictionary = []
  for e in content:
    dictionary.append({
      "word": e["pronounciation"],
      "explanation": stack(e['meaning'][1:]),
      "extension": e["meaning"][0]
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
    _d.append({"word": w["word"], "explanation": reformed, "extension": w["extension"]})
  return _d


def fix_typo_extension(d):
  _d = []
  _err = []
  for w in d:
    exs = w["extension"]
    _temp = exs.replace('n~', 'ñ')
    _temp = _temp.replace('?', w["word"][_temp.find('?')])
    e = {"word": w["word"], "explanation": w["explanation"], "extension": _temp}
    if _temp.split('/')[0] == w["word"]:
      _d.append(e)
    else:
      _err.append(e) 
  # return _d, _err
  return _d

def reform_extension(d):
  d1, d2, d3 = [], [], []
  for e in d:
    endings = e["extension"].split('/')
    if len(endings) == 2:
      if '-' in endings[1]:
        assert(endings[1] == '-a') 
        endings[1] = endings[0]+'a'
        # print(endings)
      elif endings[0][-1] == 'o':
        if endings[0] == 'médico':
          e["explanation"].append({"pos": "adj.", "meaning": "医学的"})
          endings[1] = 'médica'
          # print(endings)
        elif endings[0] == 'reo':
          endings[1] = 'rea'
          # print(endings)
        elif endings[0] == 'ventrílocuo':
          endings[1] = 'ventrílocua'
          # print(endings)
        else:
          assert(len(endings[0]) >= len(endings[1]))
          index = len(endings[1])*-1
          assert(endings[0][index] == endings[1][0])
          # print("{}-{}, {}".format(endings[0][:index], endings[0][index:], endings[1]))
          endings[1] = endings[0][:index]+endings[1]
          # print(endings)
        # write to a file
        e["extension"] = endings
        d1.append(e)
      else:
        if endings[1] != "automotriz":
          initial_letter = mapped_tonics(endings[1][0])
          index = endings[0].rfind(initial_letter)
          endings[1] = endings[0][:index]+endings[1]
        e["extension"] = endings 
        d2.append(e)
    else: # len > 2
      e["extension"] = endings 
      d3.append(e)
  writeTo('./src/d1.json', d1)
  writeTo('./src/d2.json', d2)
  writeTo('./src/d3.json', d3)
  
def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)
 

dictionary = es2cn('./src/sc-tolook.json')
distinct_dict = distinct_keys(dictionary)
reformed_explained_dict = reform_explanation(distinct_dict)
correct_dict = fix_typo_extension(reformed_explained_dict)
reform_extension(correct_dict)


