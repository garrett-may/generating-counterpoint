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
#excluded = ['bwv227.11.mxl', 'bwv248.23-2.mxl', 'bwv248.42-4.mxl', 'bwv377.mxl', 'bwv8.6.mxl', 'bwv846.mxl',
#'bwv161.6.mxl', 'bwv248.64-6.mxl', 'bwv248.64-s.mxl', 'bwv36.4-2.mxl', 'bwv432.mxl']
#corp = [path for path in corp if not any(ex in path for ex in excluded)]
#rhythm.read_rhythms_corpus(corp, debug=True)
#chords.read_chords_corpus(corp, debug=True)
#counterpoint.read_notes_corpus(corp, debug=True)


# Import the melody, and process it
filename = sys.argv[1]
song = transform.import_mid(filename)
transform.populate_measures(song)

# Compute a counterpoint melody
original_melody, generate_melody = counterpoint.algorithm(song, 4.0)

# Build a new score
score = Score()
score.insert(0, original_melody)
score.insert(0, generate_melody)

# Export the score
transform.export_mid(score, '../mid/' + filename + '_gcp')
transform.export_ly(score, '../ly/' + filename + '_gcp')
transform.export_pdf(score, '../pdf/' + filename + '_gcp')


