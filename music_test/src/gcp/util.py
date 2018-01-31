from music21.roman import romanNumeralFromChord
from music21.stream import Part
from gcp import transform
from math import isclose
import json

# Basic note names
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chord_names = ['I', '-I', 'i', '#i', 'II', '-II', 'ii', '#ii', '-ii', 'III', '-III', 'iii', '#iii', '-iii', 'IV', 'iv', '#iv', 'V', 'v', '#v', 'VI', '-VI', 'vi', '#vi', '-vi', 'VII', '-VII', 'vii', '#vii', '-vii']

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

# Unigrams
chords_unigrams = transform.import_JSON('json/chords_unigrams.json')
    
# Bigrams
chords_bigrams = transform.import_JSON('json/chords_bigrams.json')
    
# Trigrams
chords_trigrams = transform.import_JSON('json/chords_trigrams.json')
    
# Note probabilites per chord
chords_given = transform.import_JSON('json/chords_given.json')
    
# Unigrams
notes_unigrams = transform.import_JSON('json/notes_unigrams.json')
    
# Bigrams
notes_bigrams = transform.import_JSON('json/notes_bigrams.json')
    
# Trigrams
notes_trigrams = transform.import_JSON('json/notes_trigrams.json')
    
# Chord probabilites per note
notes_given = transform.import_JSON('json/notes_given.json')

# Unigrams
chords_major_unigrams = transform.import_JSON('json/chords_major_unigrams.json')
    
# Bigrams
chords_major_bigrams = transform.import_JSON('json/chords_major_bigrams.json')
    
# Trigrams
chords_major_trigrams = transform.import_JSON('json/chords_major_trigrams.json')
    
# Note probabilites per chord
chords_major_given = transform.import_JSON('json/chords_major_given.json')

# Unigrams
chords_minor_unigrams = transform.import_JSON('json/chords_minor_unigrams.json')
    
# Bigrams
chords_minor_bigrams = transform.import_JSON('json/chords_minor_bigrams.json')
    
# Trigrams
chords_minor_trigrams = transform.import_JSON('json/chords_minor_trigrams.json')
    
# Note probabilites per chord
chords_minor_given = transform.import_JSON('json/chords_minor_given.json')

assert isclose(_total(chords_unigrams), 1.0)
assert isclose(_total(chords_bigrams), 1.0)
assert isclose(_total(chords_trigrams), 1.0)
assert all(isclose(_total(values), 1.0) for key, values in chords_given.items())
assert isclose(_total(notes_unigrams), 1.0)
assert isclose(_total(notes_bigrams), 1.0)
assert isclose(_total(notes_trigrams), 1.0)
assert all(isclose(_total(values), 1.0) for key, values in notes_given.items())

def note_name(note_name):
    alt_note_names_1 = ['B#', 'D-', 'C##', 'E-', 'F-', 'E#', 'G-', 'F##', 'A-', 'G##', 'B-', 'C-']    
    alt_note_names_2 = ['D--', 'B##', 'E--', 'F--', 'D##', 'G--', 'E##', 'A--', '?', 'B--', 'C--', 'A##']    
    return (note_names[alt_note_names_1.index(note_name)] if note_name in alt_note_names_1 else 
            note_names[alt_note_names_2.index(note_name)] if note_name in alt_note_names_2 else 
            note_name)

def interval(key):
    return (note_names.index(note_name(key.tonic.name)) - note_names.index('C')) % octave
       
def notes_names(notes, key):
    return [note_names[(note_names.index(note_name(n)) - interval(key)) % octave] for n in map(note_name, notes)]
    
def roman(chord, key):
    return romanNumeralFromChord(chord, key).romanNumeral
    
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