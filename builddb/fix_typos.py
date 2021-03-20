def update_dot(es2cn):
  es2cn.vocabs.update_one({"word": "n."}, {"$set": {"word": "n"}})
  es2cn.vocabs.update_one({"word": "si."}, {"$set": {"word": "si"}})

def update_g_questionmark(es2cn):
  gu = es2cn.vocabs.find({"word": {"$regex": "g\?"}})
  for e in gu:
    old_one = e["word"]
    new_one = e["word"].replace("?", "ü")
    print(old_one)
    print(new_one)
    es2cn.vocabs.update_one({"word": old_one}, {"$set": {"word": new_one}})

def fix_typos(es2cn):
  update_dot(es2cn)
  update_g_questionmark(es2cn)


