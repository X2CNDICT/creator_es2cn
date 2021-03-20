# This is a scipt used to formalize the scr/sc-tofixed2.json

import json
import traceback
import os
import re

pos = ['n.pr.', 'm.pr.', 'm.pl.', 'f.pl.', 'm.f.', 'm.', 'f.', 'vi.', 'vt.', 'vr.', 'adj.', 'adv.', 'interj.', 'pron.', 'conj.', 'prep.', 'pl.', 'amb.', 'art.', 'impers.']

def get_json_content(filename):
  content = []
  with open(filename, 'r') as f:
    content = json.load(f)
  return content

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)



def get_noun_pl(word):
  if word[-1] in ["a", "e", "i", "o", "u", "é", "ó"]:
    return word + "s"
  elif word[-1] == "z":
    return word[:-1] + "ces"
  elif word[-1] in ["á", "é", "í", "ó", "ú"] or word[-2:] in ["ay", "ey", "oy"] or word[-1] != "s":
    return word + "es"
  elif word[-2:] in ["as", "es", "is", "os", "us", "ax", "ps"] and any(c in ["a", "e", "i", "o", "u"] for c in word[:-2]):
    return word
  elif word[-2:] in ["ás", "és", "ís", "ós", "ús"]:
    return word + "es"
  elif word[-1] == "s" and word[:-1].count("a") + word[:-1].count("e") + word[:-1].count("i") + word[:-1].count("o") + word[:-1].count("u") == 1:
    return word + "es"
  else:
    print(word)
    return None




def get_adj_pl(word):
  trans = {
    "é": "e",
    "ó": "o",
    "ú": "u",
    "ó": "o",
    "á": "a",
    "í": "i"
  }
  if word[-1] in ["a", "o", "e", "u", "i"]:
    return word + "s"
  elif word[-1] in ["á", "ó", "é", "ú", "í"]:
    return word[:-1] + trans[word[-1]] + "s"
  elif word[-1] == "z":
    return word[:-1] + "ces"
  else:
    return word + "es"

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
    item = {"word": w["word"], "explanation": reformed }
    if "extension" in w.keys():
      item["extension"] = w["extension"]
    _d.append(item)
  return _d

def fix_typo_extension(d):
	_d = []
	for w in d:
		for e in w["explanation"]:
			exs = e[1]
			_temp = exs.replace('n~', 'ñ')
			if _temp.find('?') == -1:	
				pass
			else:
				if _temp[-1] == '2' or _temp[-1] == '3':
					chn_len = len(_temp) - len(w['word']) - 1 
				else:
					chn_len = len(_temp) - len(w['word']) 
				index = _temp.find('?') - chn_len
				try:
					w["explanation"][w["explanation"].index(e)][1]= _temp.replace('?', w["word"][index])
				except Exception as exc:
					print(traceback.format_exc())
					print(exc)
					pass
		ed = {"word": w["word"], "explanation": w["explanation"]}
		_d.append(ed)
	return _d


def add_extension(d):
  extension = {'f': 'esa', 'm': 'ese', 'mpl': 'esos', 'fpl': 'esas'}
  d.append({'word': 'ese', 'explanation': [{'pos': 'adj.', 'meaning': '(阳性单数)那个', "extension": extension}]})
  d.append({'word': 'esa', 'explanation': [{'pos': 'adj.', 'meaning': '(阴性单数)那个', "extension": extension}]})
  d.append({'word': 'esos', 'explanation': [{'pos': 'adj.', 'meaning': '(阳性复数)那些', "extension": extension}]})
  d.append({'word': 'esas', 'explanation': [{'pos': 'adj.', 'meaning': '(阴性复数)那些', "extension": extension}]})

  extension = {'f': 'esta', 'm': 'este', 'mpl': 'estos', 'fpl': 'estas'}
  d.append({'word': 'este', 'explanation': [{'pos': 'adj.', 'meaning': '(阳性单数)这个', "extension": extension}]})
  d.append({'word': 'esta', 'explanation': [{'pos': 'adj.', 'meaning': '(阴性单数)这个', "extension": extension}]})
  d.append({'word': 'estos', 'explanation': [{'pos': 'adj.', 'meaning': '(阳性复数)这些', "extension": extension}]})
  d.append({'word': 'estas', 'explanation': [{'pos': 'adj.', 'meaning': '(阴性复数)这些', "extension": extension}]})

  extension = {'m': 'aquel', 'f': 'aquella', 'mpl': 'aquellos', 'fpl': 'aquellas'}
  d.append({'word': 'aquel', 'explanation': [{'pos': 'adj.', 'meaning': '(阳性单数)那个', 'extension': extension}]})
  d.append({'word': 'aquella', 'explanation': [{'pos': 'adj.', 'meaning': '(阴性单数)那个', 'extension': extension}]})
  d.append({'word': 'aquellos', 'explanation': [{'pos': 'adj.', 'meaning': '(阳性复数)那些', 'extension': extension}]})
  d.append({'word': 'aquellas', 'explanation': [{'pos': 'adj.', 'meaning': '(阴性复数)那些', 'extension': extension}]})

  d.append({'word': 'mío', 'explanation': [{'pos': 'pron.', 'meaning': '我的(用在名词单数之后)'}]})
  d.append({'word': 'mía', 'explanation': [{'pos': 'pron.', 'meaning': '我的(用在名词单数之后)'}]})
  d.append({'word': 'míos', 'explanation': [{'pos': 'pron.', 'meaning': '我的(用在名词复数之后)'}]})
  d.append({'word': 'tí', 'explanation': [{'pos': 'pron.', 'meaning': '你((用在前置词后面)'}]})
  d.append({'word': 'ustedes', 'explanation': [{'pos': 'pron.', 'meaning': '您'}]})
  d.append({'word': 'mías', 'explanation': [{'pos': 'pron.', 'meaning': '我的(用在名词复数之后)'}]})
  d.append({'word': 'pío', 'explanation': [{'pos': 'adj.', 'meaning': '虔诚的,慈善的', "extension": {'f': 'pía', 'm': 'pío', 'mpl': 'píos', 'fpl': 'pías'}}]})
  d.append({'word': 'pía', 'explanation': [{'pos': 'adj.', 'meaning': '虔诚的,慈善的', "extension": {'f': 'pía', 'm': 'pío', 'mpl': 'píos', 'fpl': 'pías'}}]})
  d.append({'word': 'Chino', 'explanation': [{'pos': 'n.pr.', 'meaning': '中国'}]})
  d.append({'word': 'colonia', 'explanation': [{'pos': 'f.', 'meaning': '移民,殖民地,花露水'}]})
  d.append({'word': 'Lima', 'explanation': [{'pos': 'n.pr.', 'meaning': '利马(秘鲁首都)'}]})
  return d


def extend(content):
  dictionary = []
  for record in content:
    es = record["explanation"] 
    if "extension" in record.keys():
      ws = record["extension"]
      assert(len(ws) == 2)
      r1 = {"word": ws[0], "explanation": []}
      r2 = {"word": ws[1], "explanation": []}
      for e in es:
        if e["pos"] in ['pron.', 'art.', 'adj.pl.']:
          explanation = {"pos": e["pos"], "meaning": e["meaning"], "extension": {"m": ws[0], "f": ws[1]}}
          r1["explanation"].append(explanation)
          r2["explanation"].append(explanation)
        elif e["pos"] == 'adj.':
          explanation = {"pos": e["pos"], "meaning": e["meaning"], "extension": {"m": ws[0], "f": ws[1], "fpl": get_adj_pl(ws[1]), "mpl": get_adj_pl(ws[0])}}
          r1["explanation"].append(explanation)
          r2["explanation"].append(explanation)
          r3 = {"word": get_adj_pl(ws[0]), "explanation": [explanation]}
          r4 = {"word": get_adj_pl(ws[1]), "explanation": [explanation]}
        elif e["pos"] == 'm.f.':
          r1["explanation"].append({"pos": 'm.', "meaning": e["meaning"], "extension": {"m": ws[0], "f": ws[1], "mpl": get_noun_pl(ws[0]), "fpl": get_noun_pl(ws[1])}})
          r2["explanation"].append({"pos": 'f.', "meaning": e["meaning"], "extension": {"m": ws[0], "f": ws[1], "mpl": get_noun_pl(ws[0]), "fpl": get_noun_pl(ws[1])}})
          r3 = {"word": get_noun_pl(ws[0]), "explanation": []}
          r4 = {"word": get_noun_pl(ws[1]), "explanation": []}
          r3["explanation"].append({"pos": 'm.pl.', "meaning": e["meaning"], "extension": {"m": ws[0], "f": ws[1], "mpl": get_noun_pl(ws[0]), "fpl": get_noun_pl(ws[1])}})
          r4["explanation"].append({"pos": 'f.pl.', "meaning": e["meaning"], "extension": {"m": ws[0], "f": ws[1], "mpl": get_noun_pl(ws[0]), "fpl": get_noun_pl(ws[1])}})
        else:
          r1["explanation"].append(e)
      # Finish iterating the explanations
      dictionary.append(r1)
      dictionary.append(r2)
      if r3 != None:
        dictionary.append(r3)
      if r4 != None:
        dictionary.append(r4)
    else:
      dictionary.append(record)
  return dictionary


def parse_extension(variation):
  endings = variation.split("/")
  if endings[1][-2:] == "-a":
    endings[1] = endings[0] + "a"
  else:
    initial_letter = endings[1][0]
    index = endings[0].rfind(initial_letter)
    endings[1] = endings[0][:index]+endings[1]
  return endings

def read(filename):
  content = get_json_content(filename)
  dictionary = []
  for e in content:
    assert(e["meaning"][0] == "1")
    meaning = stack(e["meaning"][1:])
    for m in meaning:
      s = re.match(r'(?P<chinese>[^a-z]*)(?P<spanish>[a-z\?~]+/[a-z\?~-]+)$', m[1])
      if s != None:
        m[1] = s.group("chinese")
        if e["word"] != "calidoscopio":
          e["extension"] = parse_extension(s.group("spanish"))
      else:
        s = re.sub(r'[a-z\?~2]+$', '', m[1])
        m[1] = s
    item = {
      "word": e["pronounciation"],
      "explanation": meaning
    }
    if "extension" in e.keys():
      item["extension"] = e["extension"]
    dictionary.append(item)
  return dictionary


f_origin = './src/sc-tofixed2.json' 
dictionary = read(f_origin)
distinct_dict = distinct_keys(dictionary)
reformed_explained_dict = reform_explanation(distinct_dict)
d = extend(reformed_explained_dict)
writeTo('./dst/sc-fixed2.json' , d)
