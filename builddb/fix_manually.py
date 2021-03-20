import csv
from db import DB
import json

def readCSV(filename):
  with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, skipinitialspace=True, delimiter='@')
    header = next(readCSV)
    return [dict(zip(header, row)) for row in readCSV]

def correct_wrong(x2y, records):
  for e in records:
    print(e)
    explanation = json.loads(e["explanation"].replace("\'", "\""))
    e["explanation"] = explanation
    x2y.insert_vocabs_one(e)
 
def fix_through_review(x2y):
  rs = readCSV('./dst/replace_words.csv')
  correct_wrong(x2y, rs)
  rs = readCSV('./dst/replace_explanations.csv')
  correct_wrong(x2y, rs)

if __name__ == '__main__':
  x2y = DB('es2cn', 'dict', 'turingmachine', '127.0.0.1')
  fix_through_review(x2y)
