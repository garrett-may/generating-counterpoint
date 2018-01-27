from music21.roman import romanNumeralFromChord
import json
from gcp import transform
from math import isclose

# Basic note names
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chord_names = ['I', '-I', 'i', '#i', 'II', '-II', 'ii', '#ii', '-ii', 'III', '-III', 'iii', '#iii', '-iii', 'IV', 'iv', '#iv', 'V', 'v', '#v', 'VI', '-VI', 'vi', '#vi', '-vi', 'VII', '-VII', 'vii', '#vii', '-vii']

[]

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
chord_unigrams = transform.import_JSON('json/chord_unigrams.json')
    
# Bigrams
chord_bigrams = transform.import_JSON('json/chord_bigrams.json')
    
# Trigrams
chord_trigrams = transform.import_JSON('json/chord_trigrams.json')
    
# Note probabilites per chord
chord_given = transform.import_JSON('json/chord_given.json')
    
# Unigrams
note_unigrams = transform.import_JSON('json/note_unigrams.json')
    
# Bigrams
note_bigrams = transform.import_JSON('json/note_bigrams.json')
    
# Trigrams
note_trigrams = transform.import_JSON('json/note_trigrams.json')
    
# Chord probabilites per note
note_given = transform.import_JSON('json/note_given.json')

# Unigrams
chord_major_unigrams = transform.import_JSON('json/chord_major_unigrams.json')
    
# Bigrams
chord_major_bigrams = transform.import_JSON('json/chord_major_bigrams.json')
    
# Trigrams
chord_major_trigrams = transform.import_JSON('json/chord_major_trigrams.json')
    
# Note probabilites per chord
chord_major_given = transform.import_JSON('json/chord_major_given.json')

# Unigrams
chord_minor_unigrams = transform.import_JSON('json/chord_minor_unigrams.json')
    
# Bigrams
chord_minor_bigrams = transform.import_JSON('json/chord_minor_bigrams.json')
    
# Trigrams
chord_minor_trigrams = transform.import_JSON('json/chord_minor_trigrams.json')
    
# Note probabilites per chord
chord_minor_given = transform.import_JSON('json/chord_minor_given.json')

#assert isclose(_total(chord_unigrams), 1.0)
#assert isclose(_total(chord_bigrams), 1.0)
#assert isclose(_total(chord_trigrams), 1.0)
#print(_total(chord_given))
#assert isclose(_total(chord_given), 1.0)
#assert isclose(_total(note_unigrams), 1.0)
#assert isclose(_total(note_bigrams), 1.0)
#assert isclose(_total(note_trigrams), 1.0)
#assert isclose(_total(note_given), 1.0)

def note_name(note_name):
    alt_note_names_1 = ['B#', 'D-', 'C##', 'E-', 'F-', 'E#', 'G-', 'F##', 'A-', 'G##', 'B-', 'C-']    
    alt_note_names_2 = ['D--', 'B##', 'E--', 'F--', 'D##', 'G--', 'E##', 'A--', '?', 'B--', 'C--', 'A##']    
    return (note_names[alt_note_names_1.index(note_name)] if note_name in alt_note_names_1 else 
            note_names[alt_note_names_2.index(note_name)] if note_name in alt_note_names_2 else 
            note_name)

def interval(key):
    return (note_names.index(note_name(key.tonic.name)) - note_names.index('C')) % octave
       
def notes_names(notes, key):
    return map(lambda n: note_names[(note_names.index(note_name(n)) - interval(key)) % octave], map(note_name, notes))
    
def roman(chord, key):
    return romanNumeralFromChord(chord, key).romanNumeral
    
def rotate(l, n):
    return l[-n:] + l[:-n]