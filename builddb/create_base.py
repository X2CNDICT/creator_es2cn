def create_db(x2y):
  x2y.cleanup_vocabs()
  x2y.bulk_create_vocabs('./dst/spanish-chinese.json')
  x2y.bulk_create_vocabs('./dst/tolook.json')
  x2y.bulk_create_vocabs('./dst/sc-fixed1.json')
  x2y.bulk_create_vocabs('./dst/sc-fixed4.json')
  x2y.bulk_create_vocabs('./dst/sc-fixed2.json')
  x2y.bulk_create_vocabs('./dst/sc-fixed3.json')

  x2y.cleanup_base()
  x2y.bulk_create_base('./pure/spanish-chinese.json')
  x2y.bulk_create_base('./pure/tolook.json')
  x2y.bulk_create_base('./pure/sc-fixed1.json')
  x2y.bulk_create_base('./pure/sc-fixed4.json')
  x2y.bulk_create_base('./pure/sc-fixed2.json')
  x2y.bulk_create_base('./pure/sc-fixed3.json')


def create_verbs_extension_db(x2y):
  x2y.cleanup_verbs_extension()
  x2y.bulk_create_verbs_variation('./dst/verb_variation.json')
  x2y.bulk_create_verbs_variation('./dst/verb_variation_vos.json')
  x2y.bulk_create_verbs_inverse_variation('./dst/verb_inverse_variation')
  x2y.bulk_create_verbs_inverse_variation('./dst/verb_inverse_variation_vos')

def remove_empty_vocabs(x2y):
  x2y.vocabs.delete_one({"word": ""})

def query_db(x2y):
  print(x2y.search_vocab('mal'))
 
