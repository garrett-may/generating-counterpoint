from music21.stream import Part
from music21.roman import romanNumeralFromChord

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

# Translates the note name to a particular set
# This handles notes which are "equal", such as F# and G-
def note_name(note_name):
    alt_note_names_1 = ['B#', 'D-', 'C##', 'E-', 'F-', 'E#', 'G-', 'F##', 'A-', 'G##', 'B-', 'C-']    
    alt_note_names_2 = ['D--', 'B##', 'E--', 'F--', 'D##', 'G--', 'E##', 'A--', '?', 'B--', 'C--', 'A##']    
    return (note_names[alt_note_names_1.index(note_name)] if note_name in alt_note_names_1 else 
            note_names[alt_note_names_2.index(note_name)] if note_name in alt_note_names_2 else 
            note_name)

# Gets the interval between this key and the key of C            
def interval(key):
    return (note_names.index(note_name(key.tonic.name)) - note_names.index('C')) % octave
       
# Maps a list of notes to their translated note names
# This also takes into account the key, and can include the octave if needed
def notes_names(notes, key, include_octave=False):
    return [note_names[(note_names.index(note_name(n.name)) - interval(key)) % octave] + (str(n.octave) if include_octave else '') for n in notes]
    
# Translates the chord name to a particular set
# This handles chords which are "equal", such as I and #VII
def chord_name(chord_name):
    alt_chord_names_1 = ['#VII', '-II', '?', '-III', '-IV', '#III', '-V', '?', '-VI', '?', '-VII', '-I',
                         '#vii', '-ii', '?', '-iii', '-iv', '#iii', '-v', '?', '-vi', '?', '-vii', '-i']
    return (chord_names[alt_chord_names_1.index(chord_name)] if chord_name in alt_chord_names_1 else
            chord_name)
    
# Get the roman numeral chord name from a chord
# This takes into account the key    
def roman(chord, key):
    return chord_name(romanNumeralFromChord(chord, key).romanNumeral)
    
# Builds a music21 part from a sequence of elements    
def part(sequence):
    part = Part()
    for elem in sequence:
        part.append(elem)
    return part
    
# Gets the key of a sequence
def key(sequence):
    return part(sequence).analyze('key')
    
# Checks whether a key is major or not
def is_major(key):
    return key.mode == 'major'
    
# Gets the time signature of a music21 song
def time_signature(song):
    time_signatures = [time_signature for time_signature in song.flat.getElementsByClass('TimeSignature')]
    if len(time_signatures) > 0:
        time_signature = time_signatures[0] 
        return time_signature.beatDuration.quarterLength * time_signature.numerator
    else:
        return 0.0