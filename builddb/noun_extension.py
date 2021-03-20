import re

def get_noun_pl(word):
  if word[-1] in ["a", "e", "i", "o", "u", "é", "ó"]:
    return word + "s"
  elif word[-1] == "z":
    return word[:-1] + "ces"
  elif word[-1] == "á":
    return word + "s"
  elif word[-1] in ["í", "ú"] or word[-2:] in ["ay", "ey", "oy"]:
    return word + "es"
  elif word[-1] != "s":
    word = word.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return word + "es"
  elif word[-2:] in ["as", "es", "is", "os", "us", "ax", "ps"] and any(c in ["a", "e", "i", "o", "u"] for c in word[:-2]):
    return word
  elif word[-3:] == "aís":
    return word + "es"
  elif word[-2:] in ["ás", "és", "ís", "ós", "ús"]:
    tmp = word[-2:].replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return word[:-2] + tmp + "es"
  elif word[-1] == "s" and word[:-1].count("a") + word[:-1].count("e") + word[:-1].count("i") + word[:-1].count("o") + word[:-1].count("u") == 1:
    return word + "es"
  else:
    return word + "s"

def extend_noun(es2cn):
  nouns = es2cn.search_by_pos('m.')
  for m in nouns:
    for e in m["explanation"]:
      if e["pos"] == 'm.' and "extension" not in e.keys():
        pl = get_noun_pl(m["word"])
        if pl != None:
          e["extension"] = {"mpl": pl}
          # print(m)
          es2cn.update_extension(m["_id"], m["explanation"], m["word"])
          r1 = {"word": pl, "explanation": [{"pos": "m.pl.", "meaning": e["meaning"], "extension": {"m": m["word"]}}]}
          es2cn.insert_vocabs_one(r1)

  nouns = es2cn.search_by_pos('f.')
  for m in nouns:
    if len(m["word"]) > 1:
      for e in m["explanation"]:
        reg = re.compile(r"^[子字]母.{1,2}[的]?名称$")
        if e["pos"] == 'f.' and "extension" not in e.keys() and reg.match(e["meaning"]) == None:
          pl = get_noun_pl(m["word"])
          if pl != None:
            e["extension"] = {"fpl": pl}
            # print(m)
            es2cn.update_extension(m["_id"], m["explanation"], m["word"])
            r1 = {"word": pl, "explanation": [{"pos": "f.pl.", "meaning": e["meaning"], "extension": {"f": m["word"]}}]}
            es2cn.insert_vocabs_one(r1)

  nouns = es2cn.search_by_pos('m.f.')
  for m in nouns:
    print(m)
    for e in m["explanation"]:
      if e["pos"] == 'm.f.' and "extension" not in e.keys():
        pl = get_noun_pl(m["word"])
        if pl != None:
          e["extension"] = {"pl": pl}
          # print(m)
          es2cn.update_extension(m["_id"], m["explanation"], m["word"])
          r1 = {"word": pl, "explanation": [{"pos": "m.f.pl.", "meaning": e["meaning"], "extension": {"mf": m["word"]}}]}
          es2cn.insert_vocabs_one(r1)


def test_noun(es2cn):
  nouns = es2cn.search_by_pos('m.')
  for m in nouns:
    for e in m["explanation"]:
      if e["pos"] == 'm.':
        if "extension" in e.keys():
          keys = e["extension"].keys()
          assert(len(keys) == 1 or len(keys) == 4)
          if len(keys) == 1:
            assert("mpl" in keys or "fpl" in keys)
          if len(keys) == 4:
            assert("m" in keys)
            assert("f" in keys)
            assert("mpl" in keys)
            assert("fpl" in keys)
        else:
          print(m)


