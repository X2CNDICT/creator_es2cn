import csv
from db import DB

def writeToCSV(fields, content, csvfile="distribution.csv"):
  print('Create {} file'.format(csvfile))
  with open(csvfile, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=fields, delimiter='@')
    dict_writer.writeheader()
    dict_writer.writerows(content)

def print_vocabs(es2cn, pos):
  vocabs = es2cn.search_by_pos(pos)
  for e in vocabs:
    del e["_id"]
  writeToCSV(["word", "explanation"], vocabs, pos+'csv')

if __name__ == '__main__':
  x2y = DB('es2cn', 'dict', 'turingmachine', '127.0.0.1')
  print_vocabs(x2y, 'adj.')
  print_vocabs(x2y, 'm.')
  print_vocabs(x2y, 'f.')
  print_vocabs(x2y, 'm.f.')
  print_vocabs(x2y, 'pron.')

