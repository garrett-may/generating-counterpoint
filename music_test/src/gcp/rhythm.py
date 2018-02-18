from music21.stream import *
from music21.note import Note, Rest
from music21.chord import Chord
from gcp import corpus
from gcp import transform
from gcp.transform import Hold
from gcp import util
import numpy as np
    
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
    rhythm_mapping = {Note: 'Note', Rest: 'Rest', Hold: 'Hold'}
    rhythm_types = rhythm_mapping.values()
    note_types = util.note_names
    chord_types = util.chord_names
    
    unigrams = {rhythm_1:0 for rhythm_1 in rhythm_types}
    bigrams = {rhythm_1:{rhythm_2:0 for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    trigrams = {rhythm_1:{rhythm_2:{rhythm_3:0 for rhythm_3 in rhythm_types} for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    given = {rhythm_1:{rhythm_2:0 for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key) for chord in chords]
    
    parts = transform.flatten_equalised_parts(song)
    parts = [[elem for ls in part for elem in ls] for part in parts]
    
    for part in parts:
        part = [rhythm_mapping[type(elem)] for elem in part]
        
        for i in range(0, len(part)):
            unigrams[part[i]] += 1

        # Note bigrams
        for i in range(0, len(part) - 1):
            bigrams[part[i]][part[i+1]] += 1

        # Note trigrams
        for i in range(0, len(part) - 2):
            trigrams[part[i]][part[i+1]][part[i+2]] += 1
        
    prev_notes = [Rest() for part in parts]
    for i in range(len(parts[0])):
        elems = [part[i] for part in parts]
        (curr_notes, prev_notes) = next_notes(elems, prev_notes)
        if len(elems) > 1:
            rhythm_1 = rhythm_mapping[type(elems[0])]
            for elem in elems[1:]:       
                rhythm_2 = rhythm_mapping[type(elem)]
                given[rhythm_2][rhythm_1] += 1
            
        #for index, elem in enumerate(elems):
        #    note = elems[index] if type(elems[index]) is Note else prev_notes[index]
        #    if type(note) is Note:
        #        note_name = util.notes_names([note], key)[0]
        #        elem = rhythm_mapping[type(elem)]
        #        given[elem][note_name] += 1
            
        #if curr_notes != []:
        #    chord = Chord(curr_notes)
            #chord_name = util.roman(chord, key)
            #elems = [rhythm_mapping[type(elem)] for elem in elems]
            #for elem in elems:
            #    given[elem][chord_name] += 1  
            
            
    return (unigrams, bigrams, trigrams, given)
    
def read_rhythms_corpus(corp, debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))

    # All
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(corp, populate_rhythms, filt=None, debug=debug)
   
    transform.export_JSON('json/rhythms_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(corp, populate_rhythms, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/rhythms_major_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_major_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_major_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(corp, populate_rhythms, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/rhythms_minor_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_minor_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_minor_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_minor_given.json', given)
    
def algorithm(melody, algorithm):
    (unigrams, bigrams, trigrams, given) = (transform.import_JSON('json/rhythms_major_unigrams.json'), transform.import_JSON('json/rhythms_major_bigrams.json'), transform.import_JSON('json/rhythms_major_trigrams.json'), transform.import_JSON('json/rhythms_major_given.json'))
    #transposed_melody = util.notes_names([note for note in melody], util.key(melody))
    part = transform.equalise_interval(melody)
    rhythm_mapping = {Note: 'Note', Rest: 'Rest', Hold: 'Hold'}
    part = [rhythm_mapping[type(elem)] for elem in part]
    return algorithm.algorithm(part, unigrams, bigrams, trigrams, given, rand=True)