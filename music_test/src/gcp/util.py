from music21.roman import romanNumeralFromChord
from music21.stream import Part
from gcp import transform
from math import isclose
import json

# Basic note names
note_names  = ['C', 'C#', 'D',  'D#',  'E',   'F',  'F#',  'G', 'G#', 'A',  'A#',  'B']
chord_names = ['I', '#I', 'II', '#II', 'III', 'IV', '#IV', 'V', '#V', 'VI', '#VI', 'VII',
               'i', '#i', 'ii', '#ii', 'iii', 'iv', '#iv', 'v', '#v', 'vi', '#vi', 'vii']

# Basic Roman numerals
roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

# Basic key types
key_types = ['major', 'minor']

# Octave
octave = 12

# Chromatic scale
chromatic_scale = range(0, octave)

# Circle of fifths
circle_of_fifths = [note * 7 % octave for note in chromatic_scale]

def _total(item):
    return sum(_total(i) for i in item.values()) if type(item) is dict else item




#assert isclose(_total(chords_unigrams), 1.0)
#assert isclose(_total(chords_bigrams), 1.0)
#assert isclose(_total(chords_trigrams), 1.0)
#assert all(isclose(_total(values), 1.0) or isclose(_total(values), 0.0) for key, values in chords_given.items())
#assert isclose(_total(notes_unigrams), 1.0)
#assert isclose(_total(notes_bigrams), 1.0)
#assert isclose(_total(notes_trigrams), 1.0)
#assert all(isclose(_total(values), 1.0) or isclose(_total(values), 0.0) for key, values in notes_given.items())

def note_name(note_name):
    alt_note_names_1 = ['B#', 'D-', 'C##', 'E-', 'F-', 'E#', 'G-', 'F##', 'A-', 'G##', 'B-', 'C-']    
    alt_note_names_2 = ['D--', 'B##', 'E--', 'F--', 'D##', 'G--', 'E##', 'A--', '?', 'B--', 'C--', 'A##']    
    return (note_names[alt_note_names_1.index(note_name)] if note_name in alt_note_names_1 else 
            note_names[alt_note_names_2.index(note_name)] if note_name in alt_note_names_2 else 
            note_name)

def interval(key):
    return (note_names.index(note_name(key.tonic.name)) - note_names.index('C')) % octave
       
def notes_names(notes, key, include_octave=False):
    return [note_names[(note_names.index(note_name(n.name)) - interval(key)) % octave] + (str(n.octave) if include_octave else '') for n in notes]
    
def chord_name(chord_name):
    alt_chord_names_1 = ['#VII', '-II', '?', '-III', '-IV', '#III', '-V', '?', '-VI', '?', '-VII', '-I',
                         '#vii', '-ii', '?', '-iii', '-iv', '#iii', '-v', '?', '-vi', '?', '-vii', '-i']
    return (chord_names[alt_chord_names_1.index(chord_name)] if chord_name in alt_chord_names_1 else
            chord_name)
    
def roman(chord, key):
    return chord_name(romanNumeralFromChord(chord, key).romanNumeral)
    
def rotate(l, n):
    return l[-n:] + l[:-n]
    
def part(sequence):
    part = Part()
    for elem in sequence:
        part.append(elem)
    return part
    
def key(sequence):
    return part(sequence).analyze('key')
    
def is_major(key):
    return key.mode == 'major'