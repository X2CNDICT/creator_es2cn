import json
import csv

def get_json_content(filename):
  content = []
  with open(filename, 'r') as f:
    content = json.load(f)
  return content
 
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


def es2cn(filename):
  content = get_json_content(filename)
  dictionary = []
  for record in content:
    ws = record["extension"]
    es = record["explanation"] 
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
  return dictionary

def irregular_records():
  extension = [
    {'f': 'ésa', 'm': 'ése', 'n': 'eso', 'mpl': 'ésos', 'fpl': 'ésas'},
    {'m': 'éste', 'f': 'ésta', 'n': 'esto', 'mpl': 'éstos', 'fpl': 'éstas'},
    {'m': 'aquél', 'f': 'aquélla', 'mpl': 'aquéllos', 'fpl': 'aquéllas', 'n': 'aquello'}
  ]

  d = []
  d.append({'word': 'aquél', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性单数)那个', 'extension': extension}]})
  d.append({'word': 'aquello', 'explanation': [{'pos': 'pron.', 'meaning': '(中性单复数)那个', 'extension': extension}]})
  d.append({'word': 'aquélla', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性单数)那个', 'extension': extension}]})
  d.append({'word': 'aquéllos', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性复数)那些', 'extension': extension}]})
  d.append({'word': 'aquéllas', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性复数)那些', 'extension': extension}]})

  d.append({'word': 'ése', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性单数)那个', "extension": extension}]})
  d.append({'word': 'eso', 'explanation': [{'pos': 'pron.', 'meaning': '(中性单复数)那个,那些', "extension": extension}]})
  d.append({'word': 'ésa', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性单数)那个', "extension": extension}]})
  d.append({'word': 'ésos', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性复数)那些', "extension": extension}]})
  d.append({'word': 'ésas', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性复数)那些', "extension": extension}]})

  d.append({'word': 'éste', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性单数)这个', "extension": extension}]})
  d.append({'word': 'ésta', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性单数)这个', "extension": extension}]})
  d.append({'word': 'esto', 'explanation': [{'pos': 'pron.', 'meaning': '(中性单复数)这个,这些', "extension": extension}]})
  d.append({'word': 'éstos', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性复数)这些', "extension": extension}]})
  d.append({'word': 'éstas', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性复数)这些', "extension": extension}]})

  d.append({'word': 'suyo', 'explanation': [{'pos': 'pron.', 'meaning': '他的,她的,他们的,她们的,您的,你们的'}, {'pos': 'm.', 'meaning': '他的人,他家的人'}]})
  d.append({'word': 'suya', 'explanation': [{'pos': 'pron.', 'meaning': '他的,她的,他们的,她们的,您的,你们的'}, {'pos': 'f.', 'meaning': '她的人,她家的人'}]})
  d.append({'word': 'suyos', 'explanation': [{'pos': 'pron.', 'meaning': '他的,她的,他们的,她们的,您的,你们的'}, {'pos': 'm.pl.', 'meaning': '他们的人,他们家的人'}]})
  d.append({'word': 'suyas', 'explanation': [{'pos': 'pron.', 'meaning': '他的,她的,他们的,她们的,您的,你们的'}, {'pos': 'f.pl.', 'meaning': '她们的人,她们家的人'}]})

  d.append({'word': 'tuyo', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性单数)你的(置于名词后或与ser连用)'}]})
  d.append({'word': 'tuya', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性单数)你的(置于名词后或与ser连用)'}]})
  d.append({'word': 'tuyos', 'explanation': [{'pos': 'pron.', 'meaning': '(阳性复数)你的(置于名词后或与ser连用)'}]})
  d.append({'word': 'tuyas', 'explanation': [{'pos': 'pron.', 'meaning': '(阴性复数)你的(置于名词后或与ser连用)'}]})
  return d

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)

def writeToCSV(fields, content, csvfile="distribution.csv"):
  print('Create {} file'.format(csvfile))
  with open(csvfile, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=fields, delimiter='@')
    dict_writer.writeheader()
    dict_writer.writerows(content)


def combine():
  d1 = get_json_content('./src/d1.json')
  d2 = get_json_content('./src/d2.json')

  d = d1+d2
  writeTo('./src/dn.json', d)

combine()
d = es2cn('./src/dn.json')
di = irregular_records()
writeTo('./dst/tolook.json', d+di)

