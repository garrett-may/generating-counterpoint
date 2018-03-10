from music21.note import Note
from gcp import util, transform, chords, notes, rhythm


def algorithm(song, time_signature_symbol):
    debug=True

    original_melody = [note for bar in song.elements for note in bar]
    stripped_melody = [note for bar in song.elements for note in bar if type(note) == Note]
    
    time_signature = util.time_signature(time_signature_symbol)

    # Find a chord sequence
    chord_sequence = chords.algorithm(stripped_melody, debug=debug)
    # Find a note sequence
    note_sequence = notes.algorithm(stripped_melody, chord_sequence, debug=debug)
    # Find a rhythm sequence
    rhythm_sequence = rhythm.algorithm(original_melody, debug=debug)
    
    melody_sequence = transform.note_rhythm_zip(original_melody, note_sequence, rhythm_sequence, time_signature)
    #print(melody_sequence)
    return (util.part([time_signature_symbol] + original_melody), util.part([time_signature_symbol] + melody_sequence))