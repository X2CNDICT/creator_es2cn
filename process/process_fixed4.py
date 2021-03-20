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
  # dictionary = []
  dn = []
  for e in content:
    if e['meaning'][1] in ['m.', 'f.']:
      # split into 2 records 
      endings = e['meaning'][0].split('/')
      if endings[1] == '-a':
        dn.append({'word': e['pronounciation'], 'explanation': stack(e['meaning'][1:])})
        dn.append({'word': endings[0]+'a', 'explanation': stack(['f.', e['meaning'][-1]])})
      else:
        assert(len(endings[0]) >= len(endings[1]))
        index = len(endings[1])*-1
        assert(endings[0][index] == endings[1][0])
        # print("{}-{}, {}".format(endings[0][:index], endings[0][index:], endings[1]))
        endings[1] = endings[0][:index]+endings[1]

        dn.append({'word': endings[0], 'explanation': stack(e['meaning'][1:])})
        dn.append({'word': endings[1], 'explanation': stack(['f.', e['meaning'][-1]])})

    elif e['meaning'][1] in ['adj.']:
      dn.append({'word': e['pronounciation'], 'explanation': stack(e['meaning'][1:])})
    else:
      dn.append({
        "word": e["pronounciation"],
        "explanation": stack(e['meaning'])
      })
  return dn

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
 

d = es2cn('./src/sc-tofixed4.json')

writeTo('./dst/sc-fixed4.json', reform_explanation(d))

