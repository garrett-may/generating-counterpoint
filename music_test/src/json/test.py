import csv
import json

filenames = ['chord.1stL.csv', 'chord.2ndL.csv']

mapping = {
    '1': 'I',
    '4': 'IV',
    '5': 'V',
    '6': 'vi',
    '2': 'ii',
    '3': 'iii',
    'b7': '#VI',
    'b6': '#V',
    'b3': '#II',
    '7': 'vii',
    'b4': 'iv',
    'L7': 'vii',
    'D3': '#II',
    'b5': 'v',
    'Y5': 'v',
    'b4': 'iv',
    'b1': 'i',
    'C1': 'i',
    'M1': 'I',
    'M7': '#VI',
    'M5': 'v',
    'b1': 'i',
    'M5': 'v',
    'b2': 'ii',
    'L7': 'vii',
    'D4': 'IV',
    'Y5': 'v',
    'L2': 'II',
    'L4': '#IV',
    'C1': 'i',
    'Y3': '#II',
    'M4': 'IV',
    'L5': 'V',
    'C4': 'iv',
    'D1': 'i',
    'D6': 'vi',
    'C6': '#V',
    'D2': 'ii',
    'M3': 'iii',
    'Y2': '#I',
    'Y7': '#VI',
    'C2': '#I',
    'C5': '#IV'
}

# Total sum of the values of a dictionary
def _total(item):
    return sum(_total(i) for i in item.values()) if type(item) is dict else item
    
# Converts frequency to probability (total sum will be 1.0)
def _freq_to_prob(item, total):
    return {key: _freq_to_prob(value, total) for key, value in item.items()} if type(item) is dict else item / total if total > 0.0 else 0.0

def chords_name(chord_name):
    key = chord_name
    while key != "" and key not in mapping.keys():
        key = key[:-1]
    return mapping[key] if key != '' else mapping[chord_name]

chord_names = ['I', '#I', 'II', '#II', 'III', 'IV', '#IV', 'V', '#V', 'VI', '#VI', 'VII',
               'i', '#i', 'ii', '#ii', 'iii', 'iv', '#iv', 'v', '#v', 'vi', '#vi', 'vii']

unigrams = {chord_1:0 for chord_1 in chord_names}
bigrams = {chord_1:{chord_2:0 for chord_2 in chord_names} for chord_1 in chord_names}

with open(filenames[0], 'r') as csvfile:
    reader = csv.reader(csvfile)
    lines = [row for row in reader]
    for row in lines[2:]:
        chord_1 = chords_name(row[2])
        prob = float(row[5])
        unigrams[chord_1] += prob
        
with open(filenames[1], 'r') as csvfile:
    reader = csv.reader(csvfile)
    lines = [row for row in reader]
    for row in lines[2:]:
        chord_1 = chords_name(row[2].split(',')[0])
        chord_2 = chords_name(row[2].split(',')[1])
        prob = float(row[5])
        bigrams[chord_1][chord_2] += prob
        
unigrams = _freq_to_prob(unigrams, _total(unigrams))
bigrams = _freq_to_prob(bigrams, _total(bigrams))        

def pprint(ls, tab=0):
    indent = ""
    for i in range(0, tab):
        indent += '.'
    if type(ls) is list:
        print(indent)
        for elem in ls:
            pprint(elem, tab+4)
    elif type(ls) is dict:
        print(indent)
        for key, value in ls.items():
            print('{}{}'.format(indent, key))
            pprint(value, tab+4)
    else:
        print('{}{}'.format(indent, ls))
        
pprint(unigrams)    
pprint(bigrams) 

js = json.dumps(unigrams)
with open('chords_true_unigrams.json', 'w') as fp:
    fp.write(js)
    
js = json.dumps(bigrams)
with open('chords_true_bigrams.json', 'w') as fp:
    fp.write(js)
 