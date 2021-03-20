import json

def get_json_content(filename):
  content = []
  with open(filename, 'r') as f:
    content = json.load(f)
  return content
 

def filter_pure(filename):
  content = get_json_content(filename)
  dictionary = []
  for e in content:
    explanation = []
    for ex in e["explanation"]:
      explanation.append({
        "pos": ex["pos"],
        "meaning": ex["meaning"]
      })
    dictionary.append({
      "word": e["word"],
      "explanation": explanation
    })
  return dictionary
 
def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)
 

dictionary = filter_pure('./dst/spanish-chinese.json')
writeTo('./pure/spanish-chinese.json', dictionary)

dictionary = filter_pure('./dst/tolook.json')
writeTo('./pure/tolook.json', dictionary)

dictionary = filter_pure('./dst/sc-fixed1.json')
writeTo('./pure/sc-fixed1.json', dictionary)

dictionary = filter_pure('./dst/sc-fixed2.json')
writeTo('./pure/sc-fixed2.json', dictionary)

dictionary = filter_pure('./dst/sc-fixed3.json')
writeTo('./pure/sc-fixed3.json', dictionary)

dictionary = filter_pure('./dst/sc-fixed4.json')
writeTo('./pure/sc-fixed4.json', dictionary)

