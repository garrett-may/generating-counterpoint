import json

with open('json/unigrams.json', 'r') as fp:
    unigrams = json.load(fp)

with open('json/note_prob.json', 'r') as fp:
    note_prob = json.load(fp)
    
for chord_1 in unigrams.iterkeys():
    summed = sum([freq for note,freq in note_prob[chord_1].iteritems()])
    for note,freq in note_prob[chord_1].iteritems():
        note_prob[chord_1][note] = freq / float(summed)
    print(summed)
        
print('================================================')        
        
for chord_1 in unigrams.iterkeys():
    summed = sum([freq for note,freq in note_prob[chord_1].iteritems()])
    print(summed)