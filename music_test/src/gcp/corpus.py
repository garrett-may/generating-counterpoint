from music21 import corpus
from collections import *
from gcp import util

# Total sum of the values of a dictionary
def _total(item):
    return sum(_total(i) for i in item.values()) if type(item) is dict else item
    
# Converts frequency to probability (total sum will be 1.0)
def _freq_to_prob(item, total):
    return {key: _freq_to_prob(value, total) for key, value in item.items()} if type(item) is dict else item / total
    
# Converts the information's frequency to probability
def _convert_frequency_to_probability(information):
    (unigrams, bigrams, trigrams, given) = information
    unigrams = _freq_to_prob(unigrams, float(_total(unigrams)))
    bigrams = _freq_to_prob(bigrams, float(_total(bigrams)))
    trigrams = _freq_to_prob(trigrams, float(_total(trigrams)))
    given = {chord_1: _freq_to_prob(values, float(_total(values))) for chord_1, values in given.items()}
    return (unigrams, bigrams, trigrams, given)
    
# Merges two dictionaries together by summing the values of keys
def _merge_dictionaries(this, that):
    if this == {}:
        return that
    elif that == {}:
        return this
    elif type(this) is dict and type(that) is dict:
        return {key: _merge(this[key], that[key]) for key in set(this.keys()) | set(that.keys())}
    else:
        return this + that
        
# Merges the information together        
def _merge(x, y):
    (a0, b0, c0, d0) = x
    (a1, b1, c1, d1) = y
    return (_merge_dictionaries(a0, a1),
            _merge_dictionaries(b0, b1),
            _merge_dictionaries(c0, c1),
            _merge_dictionaries(d0, d1))
                
# Populates chord frequencies for a song
def populate_chords(song, is_major):
    # Initial information
    note_types = util.note_names
    chord_types = util.chord_names
    
    unigrams = {chord_1:0 for chord_1 in chord_types}
    bigrams = {chord_1:{chord_2:0 for chord_2 in note_types} for chord_1 in chord_types}
    trigrams = {chord_1:{chord_2:{chord_3:0 for chord_3 in note_types} for chord_2 in note_types} for chord_1 in chord_types}
    given = {chord_1:{note_1:0 for note_1 in note_types} for chord_1 in chord_types}

    # Get the key
    key = song.analyze('key')
    if(util.is_major(key) != is_major):
        return (unigrams, bigram, trigrams, given)

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    # Chord unigrams
    for i in range(0, len(note_names)):
        unigrams[note_names[i]] += 1

    # Chord bigrams
    for i in range(0, len(note_names) - 1):
        bigrams[note_names[i]][note_names[i+1]] += 1

    # Chord trigrams
    for i in range(0, len(note_names) - 2):
        trigrams[note_names[i]][note_names[i+1]][note_names[i+2]] += 1
        
    # Note probabilities per chord   
    for chord in chords_naive.flat.getElementsByClass('Chord'):
        notes = util.notes_names([note.name for note in chord], key)
        chord_name = util.roman(chord, key)       
        for note_name in notes:
            given[chord_name][note_name] += 1

    return (unigrams, bigrams, trigrams, given)
        
# Populates note frequencies for a song
def populate_notes(song):
    # Initial information
    note_types = util.note_names
    chord_types = util.chord_names
    
    unigrams = {note_1:0 for note_1 in note_types}
    bigrams = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    trigrams = {note_1:{note_2:{note_3:0 for note_3 in note_types} for note_2 in note_types} for note_1 in note_types}
    given = {note_1:{chord_1:0 for chord_1 in chord_types} for note_1 in note_types}
    
    # Get the key
    key = song.analyze('key')
    if(util.is_major(key) != is_major):
        return (unigrams, bigram, trigrams, given)

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    part_names = [[util.note_name(note.name) for note in part.flat.getElementsByClass('Note')] for part in song.getElementsByClass('Part')]        
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
            given[note_name][chord_name] += 1

    return (unigrams, bigrams, trigrams, given)
    
# Reads a corpus, from a particular composer, using a particular populator function
def read_corpus(composer, populate, is_major, debug=False):
    information = ({}, {}, {}, {})
    for path in corpus.getComposer(composer):
        if debug:
            print('Parsing {} ...'.format(path))
        song = corpus.parse(path)
        information = _merge(information, populate(song, is_major))
    return _convert_frequency_to_probability(information)
            