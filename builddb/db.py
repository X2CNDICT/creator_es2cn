from pymongo import MongoClient
import json
import os
import copy

class DB:
  def __init__(self, dbname, user, password, host, authdb='admin'):
    from urllib.parse import quote_plus
    uri = "mongodb://{}:{}@{}/{}".format(quote_plus(user), quote_plus(password), host, authdb)
    self.client = MongoClient(uri)
    self.db = self.client[dbname]
    self.base = self.db.base
    self.vocabs = self.db.vocabs
    self.verbs_variation = self.db.verbs_variation 
    self.verbs_inverse_variation = self.db.verbs_inverse_variation

  def bulk_create_vocabs(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.insert_vocabs_one(e)
      print("{} records have been created".format(self.vocabs.count()))
    
  def bulk_create_base(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.insert_base_one(e)
      print("{} records have been created".format(self.vocabs.count()))
 
  def bulk_create_verbs_variation(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.verb_variation_insert_one(e)
      print("{} records have been created".format(self.verbs_variation.count()))
 
  def bulk_create_verbs_inverse_variation(self, dictionary_json_folder):
    for dictionary_json_file in os.listdir(dictionary_json_folder):
      with open(os.path.join(dictionary_json_folder, dictionary_json_file)) as f:
        content = json.load(f)
        for e in content:
          self.verb_inverse_variation_insert_one(e)
        print("{} records have been created".format(self.verbs_inverse_variation.count()))
 
  def cleanup_vocabs(self):
    self.vocabs.drop()

  def cleanup_base(self):
    self.base.drop()

  def cleanup_verbs_extension(self):
    self.verbs_variation.drop()
    self.verbs_inverse_variation.drop()

  def verb_inverse_variation_insert_one(self, e):
    w, origin = e["word"], e["extension"]["origin"]
    vocab_e = self.verbs_variation.find_one({"word": origin})
    if vocab_e != None:
      ws = w.split("/")
      for new_w in ws:
        verb_e = self.verbs_inverse_variation.find_one({"word": new_w})
        if verb_e == None:
          new_e = {"word": new_w, "extension": e["extension"]}
          print(new_e)
          self.verbs_inverse_variation.insert_one(new_e)
    else:
      print(w)
 
  def verb_variation_insert_one(self, e):
    verb_e = self.verbs_variation.find_one({"word": e["word"]})
    vocab_e = self.vocabs.find_one({"word": e["word"]})
    if vocab_e != None and verb_e == None:
      print(e)
      self.verbs_variation.insert_one(e)
   
  def insert_base_one(self, e):
    db_e = self.base.find_one({"word": e["word"]})
    print(e)
    if db_e == None:
      self.base.insert_one(e)
    else:
      explanation = copy.deepcopy(db_e["explanation"])
      explanation.extend(e["explanation"])
      self.base.update_one({"word": e["word"]}, {"$set": {"explanation": explanation}})

  def insert_vocabs_one(self, e):
    db_e = self.vocabs.find_one({"word": e["word"]})
    print(e)
    if db_e == None:
      self.vocabs.insert_one(e)
    else:
      explanation = copy.deepcopy(db_e["explanation"])
      explanation.extend(e["explanation"])
      self.vocabs.update_one({"word": e["word"]}, {"$set": {"explanation": explanation}})

  def search_vocab(self, text):
    return [e for e in self.vocabs.find({"word": text})]

  def search_by_pos(self, pos):
    return [e for e in self.vocabs.find({'explanation.pos': pos})]
  
  def search_by_meaning_pos(self, meaning, pos):
    return [e for e in self.vocabs.find({'explanation.meaning': {"$regex": meaning}, "explanation.pos": pos})]

  def update_extension(self, o_id, explanation, word):
    self.vocabs.replace_one({"_id": o_id}, {"explanation": explanation, "word": word})

