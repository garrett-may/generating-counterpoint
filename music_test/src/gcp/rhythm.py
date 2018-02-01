from music21.note import Note, Rest
from music21.chord import Chord
from gcp import corpus
from gcp import transform
from gcp import util
import numpy as np

class Hold:
    pass
    
def pprint(ls, tab=0):
    indent = ""
    for i in range(0, tab):
        indent += '.'
    if type(ls) is list:
        print(indent)
        for elem in ls:
            pprint(elem, tab+4)
    else:
        print('{}{}'.format(indent, ls))

def equalise_interval(melody):
    interval = 0.0625
    new_melody = []
    for elem in melody:
        if type(elem) is not Rest:
            new_melody += [elem] + [Hold() for i in np.arange(interval, elem.quarterLength, interval)]
        else:
            new_melody += [Rest(interval) for i in np.arange(0.0, elem.quarterLength, interval)]
    return new_melody
    
def get_equalised_parts(song):
    new_parts = []
    interval = 0.0625
    parts = [[[elem for elem in bar if type(elem) in [Note, Chord, Rest]] for bar in part.getElementsByClass('Measure')] for part in song.getElementsByClass('Part')]
    
    for index, _ in enumerate(parts[0]):
        bars = [equalise_interval(part[index]) for part in parts]
        bar_length = max([len(bar) for bar in bars])
        bars = [bar + [Rest(interval * (bar_length - len(bar)))] for bar in bars]
        for i, part in enumerate(parts):
            part[index] = bars[i]
            
    return parts
    
def next_notes(elems, last_notes):
    curr_notes = []
    for index, elem in enumerate(elems):
        if type(elem) is Note:
            curr_notes += [elem]
        elif type(elem) is Chord:
            curr_notes += [note for note in elem]
        elif type(elem) is Hold:
            notes = last_notes[index]
            if type(notes) is Note:
                curr_notes += [notes]
            elif type(notes) is Chord:
                curr_notes += [note for note in notes]
    prev_notes = []
    for index, elem in enumerate(elems):
        if type(elem) is Note or type(elem) is Chord:
            prev_notes += [elem]
        else:
            prev_notes += [last_notes[index]]
    return (curr_notes, prev_notes)
    
# Populates note frequencies for a song
def populate_rhythms(song):
    # Initial information
    rhythm_mapping = {Note: 'Note', Chord: 'Chord', Rest: 'Rest', Hold: 'Hold'}
    rhythm_types = rhythm_mapping.values()
    chord_types = util.chord_names
    
    unigrams = {rhythm_1:0 for rhythm_1 in rhythm_types}
    bigrams = {rhythm_1:{rhythm_2:0 for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    trigrams = {rhythm_1:{rhythm_2:{rhythm_3:0 for rhythm_3 in rhythm_types} for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    given = {rhythm_1:{chord_1:0 for chord_1 in chord_types} for rhythm_1 in rhythm_types}
    
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names([note.name for note in chord], key) for chord in chords]
    
    parts = get_equalised_parts(song)
    #parts = [part.flat for part in song.getElementsByClass('Part')]
    #parts = [[elem for elem in part if type(elem) in [Note, Chord, Rest]] for part in parts]
    #parts = [equalise_interval(part) for part in parts]
    #parts = [[elem for ls in part for elem in ls] for part in parts]
    
    for part in parts:
        part = [rhythm_mapping[type(elem)] for ls in part for elem in ls]
        
        for i in range(0, len(part)):
            unigrams[part[i]] += 1

        # Note bigrams
        for i in range(0, len(part) - 1):
            bigrams[part[i]][part[i+1]] += 1

        # Note trigrams
        for i in range(0, len(part) - 2):
            trigrams[part[i]][part[i+1]][part[i+2]] += 1
        
    prev_notes = [Hold() for part in parts]
    for i in range(len(parts[0])):
        elems = [part[i] for part in parts]
        (curr_notes, prev_notes) = next_notes(elems, prev_notes)
        if curr_notes != []:
            chord = Chord(curr_notes)
            chord_name = util.roman(chord, key)
            elems = [rhythm_mapping[type(elem)] for elem in elems]
            for elem in elems:
                given[elem][chord_name] += 1                
    return (unigrams, bigrams, trigrams, given)
    
def read_rhythms_corpus(composer='bach', debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))

    # All
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, populate_rhythms, filt=None, debug=debug)
   
    transform.export_JSON('json/rhythms_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, populate_rhythms, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/rhythms_major_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_major_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_major_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, populate_rhythms, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/rhythms_minor_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_minor_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_minor_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_minor_given.json', given)
    
def algorithm(chords, algorithm):
    (unigrams, bigrams, trigrams, given) = (transform.import_JSON('json/rhythms_major_unigrams.json'), transform.import_JSON('json/rhythms_major_bigrams.json'), transform.import_JSON('json/rhythms_major_trigrams.json'), transform.import_JSON('json/rhythms_major_given.json'))
    return algorithm.algorithm(chords, unigrams, bigrams, given)