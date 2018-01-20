import util
from music21 import corpus
from collections import *

def _total(item):
    return sum(total(i) for i in item.values()) if type(item) is dict else item

def _freq_to_prob(item, total):
    return {key: freq_to_prob(value, total) for key, value in item.iteritems()} if type(item) is dict else item / total

def convert_frequency_to_probability(item):    
    return _freq_to_prob(item, float(_total(item)))

def merge((a0, b0, c0, d0), (a1, b1, c1, d1)):
    return (Counter(a0) + Counter(a1),
            Counter(b0) + Counter(b1),
            Counter(c0) + Counter(c1),
            Counter(d0) + Counter(d1))

def populate_with_frequencies(song):
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    chord_names = [util.roman(chord, key) for chord in chords_naive.flat.getElementsByClass('Chord')]

    note_types = util.note_names
    chord_types = set(chord_names)
    part_names = [[util.note_name(note.name) for note in part.flat.getElementsByClass('Note')] for part in song.getElementsByClass('Part')]    
    
    unigrams = {note_1:0 for note_1 in note_types}
    bigrams = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    trigrams = {note_1:{note_2:{note_3:0 for note_3 in note_types} for note_2 in note_types} for note_1 in note_types}
    chord_prob = {note_1:{chord_1:0 for chord_1 in chord_types} for note_1 in note_types}

    for note_names in part_names:    
        # Note unigrams
        for i in range(0, len(note_names)):
            unigrams[note_names[i]] += 1

        # Note bigrams
        for i in range(0, len(note_names) - 1):
            bigrams[note_names[i]][note_names[i+1]] += 1

        # Note trigrams
        for i in range(0, len(note_names) - 2):
            trigrams[note_names[i]][note_names[i+1]][note_names[i+2]] += 1
        
    # Chord probabilities per note       
    for chord in chords_naive.flat.getElementsByClass('Chord'):
        notes = util.notes_names([note.name for note in chord], key)
        chord_name = util.roman(chord, key)       
        for note_name in notes:
            chord_prob[note_name][chord_name] += 1

    return (unigrams, bigrams, trigrams, chord_prob)

def read_notes_corpus():
    unigrams = {}
    bigrams = {}
    trigrams = {}
    chord_prob = {}

    for path in corpus.getComposer('bach'):
        print('Parsing {} ...'.format(path))
        work = corpus.parse(path)
        (unigrams, bigrams, trigrams, chord_prob) = merge(
            populate_with_frequencies(work), 
            (unigrams, bigrams, trigrams, chord_prob))

    return (convert_frequency_to_probability(unigrams), 
            convert_frequency_to_probability(bigrams), 
            convert_frequency_to_probability(trigrams),
            convert_frequency_to_probability(chord_prob))