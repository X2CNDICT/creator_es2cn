from initdb import DB

def find_no_origin_verbs(es2cn):
  rs = es2cn.verbs_inverse_variation.find()
  cache = []
  for r in rs:
    w = r["extension"]["origin"]
    verb = es2cn.vocabs.find_one({"word": w})
    if verb == None and w not in cache:
      print(w)
      cache.append(w)
  print(cache)

if __name__ == '__main__':
  es2cn = DB('es2cn', 'dict', 'turingmachine', '127.0.0.1')
  find_no_origin_verbs(es2cn)
