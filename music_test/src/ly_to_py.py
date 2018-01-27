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

from gcp import util
from gcp import transform
from gcp import chords as chords
from gcp import counterpoint as counterpoint
from gcp import genetic
from gcp import viterbi
import json

#environment.set('musicxmlPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#environment.set('midiPath', '/mnt/c/Users/garrett-may/Desktop/music_test')

filename = sys.argv[1]
song = transform.import_mid(filename)
transform.populate_measures(song)
orig_melody = [note for bar in song.elements for note in bar]
melody = [note for bar in song.elements for note in bar if type(note) == Note]
chords = chords.algorithm(melody, algorithm=genetic)
#viterbi.algorithm_melody(chords)

# Add a new part
tune = Part()
accompaniment = Part()
key = song.analyze('key')
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
    #chord = chord.transpose(interval.Interval(-24))
    accompaniment.append(chord)
    tune.append(melody[index])
    counter += 1
    
score = Score()
score.insert(0, tune)
score.insert(0, accompaniment)
transform.export_mid(score, filename)
