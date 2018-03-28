from music21 import corpus

# Corpus used here is Bach
corp = corpus.getComposer('bach')
# Filter any piece which can cause errors for our program
excluded = ['bwv227.11.mxl', 'bwv248.23-2.mxl', 'bwv248.42-4.mxl', 'bwv377.mxl', 'bwv8.6.mxl', 'bwv846.mxl',
            'bwv161.6.mxl', 'bwv248.64-6.mxl', 'bwv248.64-s.mxl', 'bwv36.4-2.mxl', 'bwv432.mxl']
corp = [path for path in corp if not any(ex in path for ex in excluded)]
no_correct = 0
print('  Gold  |  Pred  ')
print('-----------------')
for path in corp:
    song = corpus.parse(path)
    key_gold = [key for key in song.flat.getElementsByClass('Key')][0]
    key_pred = song.analyze('key')
    no_correct += int(key_gold == key_pred)
    if key_gold != key_pred:       
        print('{} | {}'.format(key_gold, key_pred))
print('Key Signature Detection accuracy: {}'.format(float(no_correct) / len(corp)))