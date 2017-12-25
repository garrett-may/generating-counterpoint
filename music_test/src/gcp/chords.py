import util
from music21 import corpus
from collections import *

def populate_with_frequencies(song, unigrams, bigrams, trigrams, note_prob):
    # Get the key
    key = song.analyze('key')
    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    # Get the chord names i.e. Roman numerals from the chords
    chord_names = [util.roman(chord, key) for chord in chords_naive.flat.getElementsByClass('Chord')]
    
    # Unigrams
    for i in range(0, len(chord_names)):
        unigrams[chord_names[i]] += 1
        
    chord_types = [chord_1 for chord_1,freq in unigrams.iteritems()]    
        
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
    chord_types = [chord_1 for chord_1,freq in unigrams.iteritems()]   

    # Change frequency into probability
    total_chord = float(sum([freq for chord_1,freq in unigrams.iteritems()]))
    for chord_1 in chord_types:
        unigrams[chord_1] /= total_chord
        for chord_2 in chord_types:
            bigrams[chord_1][chord_2] /= total_chord
            for chord_3 in chord_types:
                trigrams[chord_1][chord_2][chord_3] /= total_chord
    total_note = float(sum([freq for chord_1 in chord_types for note_name,freq in note_prob[chord_1].iteritems()]))
    for chord_1 in chord_types:               
        for note_name in util.note_names:
            note_prob[chord_1][note_name] /= total_note
        
def read_chords_corpus():
    unigrams = defaultdict(float)
    bigrams = defaultdict(lambda: defaultdict(float))
    trigrams = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    note_prob = {}
    for path in corpus.getComposer('bach'):
        print('Parsing {} ...'.format(path))
        work = corpus.parse(path)
        populate_with_frequencies(work, unigrams, bigrams, trigrams, note_prob)
    convert_frequency_to_probability(unigrams, bigrams, trigrams, note_prob)
    return (unigrams, bigrams, trigrams, note_prob)
   
    
    