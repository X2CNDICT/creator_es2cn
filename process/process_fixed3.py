import json
import csv

def get_json_content(filename):
  content = []
  with open(filename, 'r') as f:
    content = json.load(f)
  return content
 

def es2cn(filename):
  content = get_json_content(filename)
  dictionary = []
  for record in content:
    meaning = record["meaning"]
    assert(len(meaning) == 3)
    word = " ".join([record["pronounciation"], meaning[0]]) 
    explanation = [{"pos": meaning[1], "meaning": meaning[2]}]
    e = {"word": word, "explanation": explanation}
    #if '?' not in word:
    dictionary.append(e)
  return dictionary

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)

def writeToCSV(fields, content, csvfile="distribution.csv"):
  print('Create {} file'.format(csvfile))
  with open(csvfile, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=fields, delimiter='@')
    dict_writer.writeheader()
    dict_writer.writerows(content)

d = es2cn('./src/sc-tofixed3.json')
writeTo('./dst/sc-fixed3.json', d)
# writeToCSV(["word", "explanation"], dw, './wrong_tofixed3.csv')

