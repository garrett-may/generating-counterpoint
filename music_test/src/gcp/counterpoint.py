from music21 import corpus
from collections import *
from gcp import util

def _total(item):
    return sum(_total(i) for i in item.values()) if type(item) is dict else item

def _freq_to_prob(item, total):
    return {key: _freq_to_prob(value, total) for key, value in item.items()} if type(item) is dict else item / total

def convert_frequency_to_probability(x):
    (unigrams, bigrams, trigrams, given) = x
    unigrams = _freq_to_prob(unigrams, float(_total(unigrams)))
    bigrams = _freq_to_prob(bigrams, float(_total(bigrams)))
    trigrams = _freq_to_prob(trigrams, float(_total(trigrams)))
    prob = {chord_1: _freq_to_prob(values, float(_total(values))) for chord_1, values in given.items()}
    return (unigrams, bigrams, trigrams, given)

def _merge(this, that):
    if this == {}:
        return that
    elif that == {}:
        return this
    elif type(this) is dict and type(that) is dict:
        return {key: _merge(this[key], that[key]) for key in set(this.keys()) | set(that.keys())}
    else:
        return this + that
        
def merge(x, y):
    (a0, b0, c0, d0) = x
    (a1, b1, c1, d1) = y
    return (_merge(a0, a1),
            _merge(b0, b1),
            _merge(c0, c1),
            _merge(d0, d1))

def populate_with_frequencies(song):
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    chord_names = [util.roman(chord, key) for chord in chords_naive.flat.getElementsByClass('Chord')]

    note_types = util.note_names
    chord_types = util.chord_names
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
            (unigrams, bigrams, trigrams, chord_prob),
            populate_with_frequencies(work))

    return convert_frequency_to_probability((unigrams, bigrams, trigrams, chord_prob))