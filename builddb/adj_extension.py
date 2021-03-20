def get_adj_pl(word):
  trans = {
    "é": "e",
    "ó": "o",
    "ú": "u",
    "ó": "o",
    "á": "a",
    "í": "i"
  }
  if word == "":
    return word
  if word[-1] in ["a", "o", "e", "u", "i"]:
    return word + "s"
  elif word[-1] in ["á", "ó", "é", "ú", "í"]:
    return word[:-1] + trans[word[-1]] + "s"
  elif word[-1] == "z":
    return word[:-1] + "ces"
  else:
    return word + "es"

def get_adj_m_f(word):
  if word[-3:] == "ior":
    # the same
    return {"m": word, "f": word}
  elif word[-3:] in ["ote", "ete"]:
    # ote -> ota, ete -> eta
    return {"m": word, "f": word[:-1]+"a"}
  elif word[-1] == "o":
    # o -> a
    return {"m": word, "f": word[:-1]+"a"}
  elif word[-2:] in ["és", "ón", "úz", "ór", "án", "ín"]:
    trans = {
      "és": "es",
      "ón": "on",
      "úz": "uz",
      "ór": "or",
      "án": "an",
      "ín": "in"
    }
    return {"m": word, "f": word[:-2]+trans[word[-2:]]+"a"}
    # pass
  elif word[-2:] in ["es", "on", "uz", "or", "an", "in"]:
    # +a
    return {"m": word, "f": word+"a"}
  elif word[-1] in ["a", "e", "i", "o"] or word[-2:] in ["al", "ar", "az", "el", "il", "or"]:
    # the same
    return {"m": word, "f": word}
  else:
    return {"m": "", "f": ""}

# TODO: Exception, 短尾形式, mal, san, gran, galán
def _extend_adj(es2cn):
  adj = es2cn.search_by_pos('adj.')
  ws = es2cn.search_by_meaning_pos("^(一|二|三|四|五|六|七|八|九|十|百)+$", "adj.")
  for m in adj:
    if m in ws:
      pass
    else:
      for e in m["explanation"]:
        if e["pos"] == 'adj.':
          if "extension" in e.keys():
            keys = e["extension"].keys()
            assert(len(keys) >= 4)
            assert('f' in keys)
            assert('m' in keys)
            assert('fpl' in keys)
            assert('mpl' in keys) 
          else:
            # m & f
            e["extension"] = get_adj_m_f(m["word"])
            # mpl & fpl
            e["extension"]["mpl"] = get_adj_pl(e["extension"]["m"])
            e["extension"]["fpl"] = get_adj_pl(e["extension"]["f"])
            es2cn.update_extension(m["_id"], m["explanation"], m["word"])
            if e["extension"]["f"] != e["extension"]["m"]:
              r1 = {"word": e["extension"]["f"], "explanation": [{"pos": "adj.", "meaning": e["meaning"], "extension": e["extension"]}]}
              r2 = {"word": e["extension"]["mpl"], "explanation": [{"pos": "adj.", "meaning": e["meaning"], "extension": e["extension"]}]}
              r3 = {"word": e["extension"]["fpl"], "explanation": [{"pos": "adj.", "meaning": e["meaning"], "extension": e["extension"]}]}
              es2cn.insert_vocabs_one(r1)
              es2cn.insert_vocabs_one(r2)
              es2cn.insert_vocabs_one(r3)
            else:
              r = {"word": e["extension"]["mpl"], "explanation": [{"pos": "adj.", "meaning": e["meaning"], "extension": e["extension"]}]}
              es2cn.insert_vocabs_one(r)
  
def _clean_adj_empty_extension(es2cn):
  adj = es2cn.search_by_pos('adj.')
  for m in adj:
    for e in m["explanation"]:
      if e["pos"] == 'adj.':
        if "extension" in e.keys():
          extension = e["extension"]
          if extension["f"]== "" and extension["m"]=="" and extension["fpl"]=="" and extension["mpl"]=="":
            del e["extension"]
            es2cn.vocabs.update_one({"word": m["word"]}, {"$set": {"explanation": m["explanation"]}})

def _test_adj(es2cn):
  adj = es2cn.search_by_pos('adj.')
  for m in adj:
    for e in m["explanation"]:
      if e["pos"] == 'adj.':
        if "extension" in e.keys():
          keys = e["extension"].keys()
          assert(len(keys) >= 4)
          assert('f' in keys)
          assert('m' in keys)
          assert('fpl' in keys)
          assert('mpl' in keys) 
        else:
          print(m)

def extend_adj(es2cn):
  _extend_adj(es2cn)
  _clean_adj_empty_extension(es2cn)
  _test_adj(es2cn)


