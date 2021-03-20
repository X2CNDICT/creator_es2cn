sujeto_personal = [
  ['yo', 'yo', 'nosotros', 'nosotras'],
  ['tú', 'tú', 'vosotros', 'vosotras'],
  ['él', 'ella', 'ellos', 'ellas'],
  ['usted', 'usted', 'ustedes', 'ustedes']
]

complemento_directo_personal = [
  ['me', 'me', 'nos', 'nos'],
  ['te', 'te', 'os', 'os'],
  ['lo', 'la', 'los', 'las']
]

complemento_indirecto_personal = [
  ['me', 'nos'],
  ['te', 'os'],
  ['le', 'les']
]

reflexivo_personal = [
  ['me', 'nos'],
  ['te', 'os'],
  ['se', 'se']
]

ablativo_personal = [
  ['mí', 'mí', 'nuestros', 'nuestras'],
  ['tí', 'tí', 'vuestros', 'vuestras'],
  ['él', 'ella', 'ellos', 'ellas'],
  ['usted', 'usted', 'ustedes', 'ustedes']
]

posesivo = [
  [['mío', 'míos'], ['mía','mías'], ['nuestro', 'nuestros'], ['nuestra', 'nuestras']],
  [['tuyo', 'tuyos'], ['tuya', 'tuyas'], ['vuestro', 'vuestros'], ['vuestra', 'vuestras']],
  [['suyo', 'suyos'], ['suya', 'suyas'], ['suyo', 'suyos'], ['suya', 'suyas']]
]


extension = {
  "sujeto_personal": sujeto_personal,
  "complemento_directo_personal": complemento_directo_personal,
  "complemento_indirecto_personal": complemento_indirecto_personal,
  "reflexivo_personal": reflexivo_personal,
  "ablativo_personal": ablativo_personal,
  "posesivo": posesivo
}

words = {
  "yo": ["sujeto_personal"],
  "tú": ["sujeto_personal"],
  "nosotros": ["sujeto_personal"],
  "nosotras": ["sujeto_personal"],
  "él" : ["sujeto_personal", "ablativo_personal"],
  "ella" : ["sujeto_personal", "ablativo_personal"],
  "ellos" : ["sujeto_personal", "ablativo_personal"],
  "ellas" : ["sujeto_personal", "ablativo_personal"],
  "usted" : ["sujeto_personal", "ablativo_personal"],
  "ustedes" : ["sujeto_personal", "ablativo_personal"],
  "me": ["complemento_directo_personal", "complemento_indirecto_personal", "reflexivo_personal"],
  "nos": ["complemento_directo_personal", "complemento_indirecto_personal", "reflexivo_personal"],
  "te": ["complemento_directo_personal", "complemento_indirecto_personal", "reflexivo_personal"],
  "os": ["complemento_directo_personal", "complemento_indirecto_personal", "reflexivo_personal"],
  "lo": ["complemento_directo_personal"],
  "los": ["complemento_directo_personal"],
  "la": ["complemento_directo_personal"],
  "las": ["complemento_directo_personal"],
  "le": ["complemento_indirecto_personal"],
  "les": ["complemento_indirecto_personal"],
  "se": ["reflexivo_personal"],
  "mí": ["ablativo_personal"],
  "tí": ["ablativo_personal"],
  "nuestros": ["ablativo_personal", "posesivo"],
  "nuestras": ["ablativo_personal", "posesivo"],
  "vuestros": ["ablativo_personal", "posesivo"],
  "vuestras": ["ablativo_personal", "posesivo"],
  "mío": ["posesivo"],
  "míos": ["posesivo"],
  "mía": ["posesivo"],
  "mías": ["posesivo"],
  "tuyo": ["posesivo"],
  "tuyos": ["posesivo"],
  "tuya": ["posesivo"],
  "tuyas": ["posesivo"],
  "suyo": ["posesivo"],
  "suyos": ["posesivo"],
  "suya": ["posesivo"],
  "suyas": ["posesivo"],
  "nuestro": ["posesivo"],
  "nuestra": ["posesivo"],
  "vuestro": ["posesivo"],
  "vuestra": ["posesivo"],
}


def extend_pron(es2cn):
  for w, tips in words.items(): 
    r = es2cn.vocabs.find_one({"word": w})
    if r != None:
      explanation = r["explanation"]
      for e in explanation:
        if e["pos"] == "pron.":
          e["extension"] = extension
          e["tips"] = tips
      es2cn.vocabs.update_one({"word": w}, {"$set": {"explanation": explanation}})
    else:
      print(w)
