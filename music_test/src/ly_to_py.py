import sys
from music21 import *
from music21.stream import *
from music21.meter import *
from music21.note import *
from music21.note import *
from music21.key import *
from music21.chord import *
from music21.roman import *
from music21.pitch import *
from music21.interval import *
from music21.corpus import getComposer

from gcp import util
from gcp import transform
from gcp import chords
from gcp import notes
from gcp import counterpoint
from gcp import genetic
from gcp import viterbi
from gcp import rhythm
import json

#environment.set('musicxmlPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#environment.set('midiPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#corp = getComposer('bach')
#excluded = ['bwv227.11.mxl', 'bwv248.23-2.mxl', 'bwv248.42-4.mxl', 'bwv377.mxl', 'bwv8.6.mxl', 'bwv846.mxl']
#corp = [path for path in corp if not any(ex in path for ex in excluded)]
#rhythm.read_rhythms_corpus(corp, debug=True)
#chords.read_chords_corpus(corp, debug=True)
#counterpoint.read_notes_corpus(corp, debug=True)


filename = sys.argv[1]
song = transform.import_mid(filename)
transform.populate_measures(song)

original_melody, generate_melody = counterpoint.algorithm(song, 3.0)

tune = original_melody
accompaniment = generate_melody

#melody = [note for bar in song.elements for note in bar if type(note) == Note]

#print(equalise_interval(orig_melody))

#chords = chords.algorithm(melody)
#chords = reversed(chords.algorithm([note for note in reversed(melody)], algorithm=viterbi))
#mel = notes.algorithm(melody, chords)
#mel = list(reversed(counterpoint.algorithm(list(reversed(melody)), list(reversed(chords)), algorithm=viterbi)))
#print(mel)
#'rhy = rhythm.algorithm(orig_melody)

# Add a new part
"""
tune = Part()
accompaniment = Part()
key = song.analyze('key')
"""
"""
current_note = None
last_rhythm_type = '????'
rhythm_length = 0.0
bar_length = 0.0
new_melody = []
interval = 0.0625
time_sig = 4.0
for rhythm_type in rhy:
    if rhythm_type != last_rhythm_type:
        if rhythm_type != 'Hold' and current_note != None:
            if bar_length + rhythm_length > time_sig:
                current_note.quarterLength = time_sig - bar_length
                rhythm_length -= (time_sig - bar_length)
                bar_length = 0.0
            else:
                current_note.quarterLength = rhythm_length
            
            new_melody += [current_note]
    if rhythm_type == 'Note':
        # Do something
        current_note = Note('C3')
        rhythm_length = interval
    elif rhythm_type == 'Hold':
        # Do something
        if current_note != None:
            rhythm_length += interval
    elif rhythm_type == 'Rest':
        # Do something
        if last_rhythm_type == 'Rest':
            rhythm_length += interval
        else:
            current_note = Rest()
            rhythm_length = interval
    last_rhythm_type = rhythm_type
if current_note != None:
    if bar_length + rhythm_length > time_sig:
        current_note.quarterLength = time_sig - bar_length
        rhythm_length -= (time_sig - bar_length)
        bar_length = 0.0
    else:
        current_note.quarterLength = rhythm_length
    
    new_melody += [current_note]   
    
tune = util.part(orig_melody)
accompaniment = util.part(new_melody)
"""
"""
print(key)
counter = 0
for index, chord_1 in enumerate(chords):
    while type(orig_melody[counter]) != Note:
        counter += 1
        rest = Rest()
        rest.quarterLength == orig_melody[counter].quarterLength
        accompaniment.append(rest)
        tune.append(rest)
    rn = roman.RomanNumeral(chord_1, key)
    chord = Chord([pitch.name + '3' for pitch in rn.pitches])
    chord.quarterLength = melody[index].quarterLength
    note = Note(mel[index])
    note.quarterLength = melody[index].quarterLength
    accompaniment.append(note)
    tune.append(melody[index])
    counter += 1
"""

score = Score()
score.insert(0, tune)
score.insert(0, accompaniment)
transform.export_mid(score, '../mid/' + filename + '_gcp')
transform.export_ly(score, '../ly/' + filename + '_gcp')
transform.export_pdf(score, '../pdf/' + filename + '_gcp')


