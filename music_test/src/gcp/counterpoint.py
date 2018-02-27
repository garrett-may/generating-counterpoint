from music21.note import Note, Rest

from gcp import util
from gcp import transform
from gcp import chords
from gcp import notes
from gcp import rhythm


def algorithm(song, time_signature):
    original_melody = [note for bar in song.elements for note in bar]
    stripped_melody = [note for bar in song.elements for note in bar if type(note) == Note]

    # Find a chord sequence
    chord_sequence = chords.algorithm(stripped_melody)
    # Find a note sequence
    note_sequence = notes.algorithm(stripped_melody, chord_sequence)
    # Find a rhythm sequence
    rhythm_sequence = rhythm.algorithm(original_melody)
    
    melody_sequence = transform.note_rhythm_zip(original_melody, note_sequence, rhythm_sequence, time_signature)
    #print(melody_sequence)
    return (util.part(original_melody), util.part(melody_sequence))