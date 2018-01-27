from gcp import util
from music21 import corpus
from collections import *

def populate_with_frequencies(song, unigrams, bigrams, trigrams, note_prob, is_major):
    # Get the key
    key = song.analyze('key')
    if((key.mode == 'major') != is_major):
        return
    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    # Get the chord names i.e. Roman numerals from the chords
    chord_names = [util.roman(chord, key) for chord in chords_naive.flat.getElementsByClass('Chord')]
    
    # Unigrams
    for i in range(0, len(chord_names)):
        unigrams[chord_names[i]] += 1
        
    chord_types = [chord_1 for chord_1,freq in unigrams.items()]    
        
    for chord_1 in chord_types:
        unigrams[chord_1] = unigrams.get(chord_1, 0)    
        
    # Bigrams
    for i in range(0, len(chord_names) - 1):
        next_chords = bigrams.get(chord_names[i], defaultdict(float))
        next_chords[chord_names[i+1]] += 1
        bigrams[chord_names[i]] = next_chords    
    for chord_1 in chord_types:
        for chord_2 in chord_types:
            bigrams[chord_1][chord_2] = bigrams.get(chord_1, {}).get(chord_2, 0)
        
    # Trigrams
    for i in range(0, len(chord_names) - 2):
        next_chords = trigrams.get(chord_names[i], defaultdict(lambda: defaultdict(float)))
        next_next_chords = next_chords.get(chord_names[i+1], defaultdict(float))
        next_next_chords[chord_names[i+2]] += 1
        next_chords[chord_names[i+1]] = next_next_chords
        trigrams[chord_names[i]] = next_chords
    for chord_1 in chord_types:
        for chord_2 in chord_types:
            for chord_3 in chord_types:
                trigrams[chord_1][chord_2][chord_3] = trigrams.get(chord_1, {}).get(chord_2, {}).get(chord_3, 0)

    # Note probabilities per chord
    for chord in chords_naive.flat.getElementsByClass('Chord'):
        notes = util.notes_names([note.name for note in chord], key)
        chord_name = util.roman(chord, key)       
        for note_name in notes:
            note_prob[chord_name] = note_prob.get(chord_name, defaultdict(float))
            note_prob[chord_name][note_name] += 1
    for chord_1 in chord_types:
        for note_name in util.note_names:
            note_prob[chord_1][note_name] = note_prob.get(chord_1, {}).get(note_name, 0)
                
def convert_frequency_to_probability(unigrams, bigrams, trigrams, note_prob):
    chord_types = [chord_1 for chord_1,freq in unigrams.items()]   

    # Change frequency into probability
    total_1 = float(sum([freq for chord_1,freq in unigrams.items()]))
    total_2 = float(sum([freq for chord_1,n_chords in bigrams.items() for chord_2,freq in n_chords.items()]))
    total_3 = float(sum([freq for chord_1,n_chords in trigrams.items() for chord_2,nn_chords in n_chords.items() for chord_3,freq in nn_chords.items()]))
    for chord_1 in chord_types:
        unigrams[chord_1] /= total_1
        for chord_2 in chord_types:
            bigrams[chord_1][chord_2] /= total_2
            for chord_3 in chord_types:
                trigrams[chord_1][chord_2][chord_3] /= total_3
    for chord_1 in chord_types:            
        total_note = float(sum([freq for note_name,freq in note_prob[chord_1].items()]))
        for note_name in util.note_names:
            note_prob[chord_1][note_name] /= total_note
        
def read_chords_corpus(is_major):
    unigrams = defaultdict(float)
    bigrams = defaultdict(lambda: defaultdict(float))
    trigrams = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    note_prob = {}
    for path in corpus.getComposer('bach'):
        print('Parsing {} ...'.format(path))
        work = corpus.parse(path)
        populate_with_frequencies(work, unigrams, bigrams, trigrams, note_prob, is_major)
    convert_frequency_to_probability(unigrams, bigrams, trigrams, note_prob)
    return (unigrams, bigrams, trigrams, note_prob)
    
def pprint(ind, song):
    opt_deque = deque(ind)      

    bars_with_chords = []
    for bar in song.elements:
        bar_with_chords = []
        for note in bar:
            if type(note) == Note:
                bar_with_chords += [opt_deque.popleft()]    
        bars_with_chords += [bar_with_chords]
    for bar_with_chords in bars_with_chords:
        print('Bar')
        for chord in bar_with_chords:
            print('{}:{}'.format(chord, roman.RomanNumeral(chord, key).pitches))
       
        
    