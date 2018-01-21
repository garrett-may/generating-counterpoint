from music21.roman import romanNumeralFromChord
import json

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

# Unigrams
with open('json/chord_unigrams.json', 'r') as fp:
    chord_unigrams = json.load(fp)
    
# Bigrams
with open('json/chord_bigrams.json', 'r') as fp:
    chord_bigrams = json.load(fp)  
    
# Trigrams
with open('json/chord_trigrams.json', 'r') as fp:
    chord_trigrams = json.load(fp)
    
# Note probabilites per chord
with open('json/chord_given.json', 'r') as fp:
    chord_given = json.load(fp)
    
# Unigrams
with open('json/note_unigrams.json', 'r') as fp:
    note_unigrams = json.load(fp)
    
# Bigrams
with open('json/note_bigrams.json', 'r') as fp:
    note_bigrams = json.load(fp)  
    
# Trigrams
with open('json/note_trigrams.json', 'r') as fp:
    note_trigrams = json.load(fp)
    
# Chord probabilites per note
with open('json/note_given.json', 'r') as fp:
    note_given = json.load(fp)

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