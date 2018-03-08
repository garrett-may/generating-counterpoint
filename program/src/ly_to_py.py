from music21.stream import Score
from music21.corpus import getComposer
from gcp import util, transform, chords, notes, rhythm, counterpoint
import sys

# You may need to set the following environment variables for music21:
#environment.set('musicxmlPath', '/<path-to-folder>/program')
#environment.set('midiPath', '/<path-to-folder>/program')

# Reads the chords corpus, notes corpus, and rhythm corpus
def read_all_corpus():
    # Corpus used here is Bach
    corp = getComposer('bach')
    # Filter any piece which can cause errors for our program
    excluded = ['bwv227.11.mxl', 'bwv248.23-2.mxl', 'bwv248.42-4.mxl', 'bwv377.mxl', 'bwv8.6.mxl', 'bwv846.mxl',
                'bwv161.6.mxl', 'bwv248.64-6.mxl', 'bwv248.64-s.mxl', 'bwv36.4-2.mxl', 'bwv432.mxl']
    corp = [path for path in corp if not any(ex in path for ex in excluded)]
    
    # Read the corpus
    chords.read_chords_corpus(corp, debug=True)
    notes.read_notes_corpus(corp, debug=True)
    rhythm.read_rhythms_corpus(corp, debug=True)
    
# Attempt to generate counterpoint, and export the result as midi file, Lilypond file, and PDF file
def generate_counterpoint_attempt():        
    # Import the melody, and process it
    filename = sys.argv[1]
    song = transform.import_mid(filename)
    time_signature = util.time_signature(song)
    transform.populate_measures(song)

    # Compute a counterpoint melody
    original_melody, generate_melody = counterpoint.algorithm(song, time_signature)

    # Build a new score
    score = Score()
    score.insert(0, original_melody)
    score.insert(0, generate_melody)

    # Export the score
    transform.export_mid(score, filename + '_gcp')
    transform.export_ly(score, filename + '_gcp')
    transform.export_pdf(score, filename + '_gcp')
    
generate_counterpoint_attempt()