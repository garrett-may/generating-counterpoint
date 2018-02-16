from music21 import corpus
from collections import *
from gcp import util

# Total sum of the values of a dictionary
def _total(item):
    return sum(_total(i) for i in item.values()) if type(item) is dict else item
    
# Converts frequency to probability (total sum will be 1.0)
def _freq_to_prob(item, total):
    return {key: _freq_to_prob(value, total) for key, value in item.items()} if type(item) is dict else item / total if total > 0.0 else 0.0
    
# Converts the information's frequency to probability
def _convert_frequency_to_probability(information):
    (unigrams, bigrams, trigrams, given) = information
    unigrams = _freq_to_prob(unigrams, float(_total(unigrams)))
    bigrams = _freq_to_prob(bigrams, float(_total(bigrams)))
    trigrams = _freq_to_prob(trigrams, float(_total(trigrams)))
    given = {key: _freq_to_prob(values, float(_total(values))) for key, values in given.items()}
    return (unigrams, bigrams, trigrams, given)
    
# Merges two dictionaries together by summing the values of keys
def _merge_dictionaries(this, that):
    if this == {}:
        return that
    elif that == {}:
        return this
    elif type(this) is dict and type(that) is dict:
        return {key: _merge_dictionaries(this[key], that[key]) for key in set(this.keys()) | set(that.keys())}
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
def populate_chords(song):
    # Initial information
    chord_types = util.chord_names
    note_types = util.note_names    
    
    unigrams = {chord_1:0 for chord_1 in chord_types}
    bigrams = {chord_1:{chord_2:0 for chord_2 in chord_types} for chord_1 in chord_types}
    trigrams = {chord_1:{chord_2:{chord_3:0 for chord_3 in chord_types} for chord_2 in chord_types} for chord_1 in chord_types}
    given = {chord_1:{note_1:0 for note_1 in note_types} for chord_1 in chord_types}

    # Get the key
    key = song.analyze('key')    

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key) for chord in chords]
    
    # Chord unigrams
    for i in range(0, len(chord_names)):
        unigrams[chord_names[i]] += 1

    # Chord bigrams
    for i in range(0, len(chord_names) - 1):
        bigrams[chord_names[i]][chord_names[i+1]] += 1

    # Chord trigrams
    for i in range(0, len(chord_names) - 2):
        trigrams[chord_names[i]][chord_names[i+1]][chord_names[i+2]] += 1
        
    # Note probabilities per chord   
    for chord_name, note_names in zip(chord_names, note_names_list):
        for note_name in note_names:
            given[chord_name][note_name] += 1

    return (unigrams, bigrams, trigrams, given)
        
# Populates note frequencies for a song
def populate_notes(song):
    # Initial information
    note_types = [note_name + str(octave) for note_name in util.note_names for octave in range(0, 8)]
    chord_types = util.chord_names
    
    unigrams = {note_1:0 for note_1 in note_types}
    bigrams = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    trigrams = {note_1:{note_2:{note_3:0 for note_3 in note_types} for note_2 in note_types} for note_1 in note_types}
    given = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key, include_octave=True) for chord in chords]
    
    part_names = [util.notes_names(part.flat.getElementsByClass('Note'), key, include_octave=True) for part in song.getElementsByClass('Part')]        
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
    for chord_name, note_names in zip(chord_names, note_names_list):
        #if len(note_names) > 1:
        #    for note_name in note_names[1:]:
        #        given[note_name][note_names[0]] += 1
        for note_name in note_names:
            given[note_name][chord_name] += 1

    return (unigrams, bigrams, trigrams, given)
    
# Reads a corpus, from a particular composer, using a particular populator function
def read_corpus(corp, populate, filt=None, debug=False):
    information = ({}, {}, {}, {})
    for path in corp:
    #for path in filter(lambda p: 'bwv248.42-4.mxl' in p, corpus.getComposer(composer)):
        if debug:
            print('Parsing {} ...'.format(path))
        song = corpus.parse(path)
        if filt != None and not filt(song):
            continue
        information = _merge(information, populate(song))
    return _convert_frequency_to_probability(information)
            