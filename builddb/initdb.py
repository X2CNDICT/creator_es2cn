from db import DB
from create_base import create_db, create_verbs_extension_db, remove_empty_vocabs
from adj_extension import extend_adj
from noun_extension import extend_noun
from pron_extension import extend_pron
from fix_typos import fix_typos
from refine_meaning import refine_meaning
from validatedb import clean_up 
from fix_manually import fix_through_review

def create_from_origin(x2y):
  create_db(x2y)
  fix_typos(x2y)
  refine_meaning(x2y)

def extension_from_origin(x2y):
  extend_adj(x2y)
  extend_noun(x2y)
  extend_pron(x2y)
  remove_empty_vocabs(x2y)

if __name__ == '__main__':
  x2y = DB('es2cn', 'dict', 'turingmachine', '127.0.0.1')
  create_from_origin(x2y)  
  clean_up(x2y)
  fix_through_review(x2y)
  extension_from_origin(x2y)
  create_verbs_extension_db(x2y)
  #query_db(x2y)
