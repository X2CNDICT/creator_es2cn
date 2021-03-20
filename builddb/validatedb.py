from db import DB
import re
import csv

def writeToCSV(fields, content, csvfile="distribution.csv"):
  print('Create {} file'.format(csvfile))
  with open(csvfile, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=fields, delimiter='@')
    dict_writer.writeheader()
    dict_writer.writerows(content)


def validate_base(x2y):
  snapshot = x2y.vocabs.find({})
  wrong_words = []
  wrong_explanations = []
  for w in snapshot:
    if w["word"] == "":
      print(w)
    if re.match(r".*[?\(\),~]+.*", w["word"]):
      del w['_id']
      wrong_words.append(w)
    exs = w["explanation"]
    for e in exs:
      print(w)
      if re.match(r".*[a-zA-Z0-9\?]+.*", e["meaning"]):
        del w['_id']
        wrong_explanations.append(w)
        break
  fields = ['word', 'explanation']
  writeToCSV(fields, wrong_words, './wrong_words.csv')
  writeToCSV(fields, wrong_explanations, './wrong_explanations.csv')
  return (wrong_words, wrong_explanations)

def delete_wrong(x2y, records):
  for e in records:
    x2y.vocabs.delete_one({"word": e["word"]})
    
def clean_up(x2y):
  w1, w2 = validate_base(x2y)
  delete_wrong(x2y, w1)
  delete_wrong(x2y, w2)

if __name__ == '__main__':
  x2y = DB('es2cn', 'phoenix', 'turingmachine', '127.0.0.1')
  clean_up(x2y)
