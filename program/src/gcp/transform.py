from music21 import converter, lily
from music21.stream import Measure
from music21.note import Note, Rest
from music21.chord import Chord
from music21.meter import TimeSignature
from gcp import util
import copy
import collections
from collections import Iterable
import json
import numpy as np

# Class to represent a held note
class Hold:
    pass

# Imports .mid to music21 song
def import_mid(filename):
    print('Start parsing...')
    song = converter.parse(filename + '.mid')
    print('End parsing')
    return song
    
# Exports music21 song to .mid
def export_mid(song, filename):
    song.write('midi', filename + '.mid')
    
# Exports music21 song to .ly
def export_ly(song, filename):
    lpc = lily.translate.LilypondConverter()
    lpMusicList = lily.lilyObjects.LyMusicList()
    lpc.context = lpMusicList
    lpc.appendObjectsToContextFromStream(song)
    
    with open(filename + '.ly', 'w') as file:
        file.write(str(lpc.context))
        
# Imports .json to Python dict
def import_JSON(filename):
    with open(filename, 'r') as fp:
        r = json.load(fp)
    return r
    
# Exports Python dict to .json    
def export_JSON(filename, w):
    js = json.dumps(w)
    with open(filename, 'w') as fp:
        fp.write(js)
    
# Exports music21 song to .pdf    
def export_pdf(song, filename):
    lpc = lily.translate.LilypondConverter()
    lpMusicList = lily.lilyObjects.LyMusicList()
    lpc.context = lpMusicList
    lpc.appendObjectsToContextFromStream(song)
    
    lpc.createPDF(filename)
        
# Some LilyPond files won't populate the measures/bars
# If this is the case, populate them
def populate_measures(song):
    # Initial values
    time_signature_length = util.time_signature(song)
    seen_length = 0
    bars = []
    current_bar = []
    
    # Helper functions
    
    # Appends an item to a bar
    def append_bar(current_bar, seen_length, item):
        current_bar += [item]
        seen_length += item.duration.quarterLength
        return (current_bar, seen_length)
    
    # Checks to see if the item finishes the bar
    def check_bar(bars, current_bar, seen_length):
        if seen_length >= time_signature_length:
            bars += [current_bar]
            current_bar = []
            seen_length = 0
        return (bars, current_bar, seen_length)
    
    # Finds the notes
    def find_bars(part):
        if isinstance(part, Iterable):
            for item in part:
                if type(item) is Note:
                    return part
                else:
                    res = find_bars(item)
                    if res is not None:
                        return res            
        return None
        
    # Find the part which has the notes
    part = find_bars(song)
    # Search through each item in the bar
    for item in part:
        if type(item) is Note:
            # Note
            (current_bar, seen_length) = append_bar(current_bar, seen_length, item)
            (bars, current_bar, seen_length) = check_bar(bars, current_bar, seen_length)
        elif type(item) is Rest:
            # Rest
            (current_bar, seen_length) = append_bar(current_bar, seen_length, item)
            (bars, current_bar, seen_length) = check_bar(bars, current_bar, seen_length)
            
    # LilyPond might forget a rest at the end
    if time_signature_length - seen_length > 0:
        (current_bar, seen_length) = append_bar(current_bar, seen_length, Rest(quarterLength = time_signature_length - seen_length))
    (bars, current_bar, seen_length) = check_bar(bars, current_bar, seen_length)
    
    # Populate song.elements, which is where the items should have been
    song.elements = []
    for bar in bars:
        measure = Measure()
        for n in bar:
            measure.append(copy.deepcopy(n))
        song.append(measure)
    return song
    
# Transforms melodies such that they are incremented by equal time intervals
# E.g. A crotchet may be split into [Note, Hold, Hold, Hold], where each element
# has a time interval of a semiquaver        
def equalise_interval(melody, interval=0.25):    
    def parse_elem(elem):
        return ([elem] + [Hold() for i in np.arange(interval, elem.quarterLength, interval)] if type(elem) is not Rest else
                [Rest(quarterLength=interval) for i in np.arange(0.0, elem.quarterLength, interval)])    
    
    return [e for elem in melody for e in parse_elem(elem)]
    
# Flattens a song into melodies, and then time interval equalises them
def flatten_equalised_parts(song, interval=0.25):
    # Only look at notes, and rests (not e.g. chords, time signature, key signature, page layouts)
    parts = [[[elem for elem in bar if type(elem) in [Note, Rest]] for bar in part.getElementsByClass('Measure')] for part in song.getElementsByClass('Part')]
    
    # Fix melodies with errors
    for index, _ in enumerate(parts[0]):
        # Get the current bars
        bars = [equalise_interval(part[index], interval) for part in parts]
        bar_length = max([len(bar) for bar in bars])
        # Fix bars which for some reason don't fill the whole bar
        # Add rests instead
        bars = [bar + [Rest(interval * (bar_length - len(bar)))] for bar in bars]
        for i, part in enumerate(parts):
            part[index] = bars[i]
            
    return parts
    
# Makes a note sequence mimic a melody in terms of quarter lengths and rests
def mimic_melody(note_sequence, melody):
    melody_sequence = []
    queue = collections.deque(note_sequence)
    for elem in melody:
        if type(elem) is Note:
            melody_sequence += [Note(queue.popleft(), quarterLength=elem.quarterLength)]
        elif type(elem) is Rest:
            melody_sequence += [Rest(quarterLength=elem.quarterLength)]
    return melody_sequence

# Zips together a note sequence and a rhythm sequence
def note_rhythm_zip(melody, note_sequence, rhythm_sequence, time_signature, interval=0.25):
    melody_sequence = mimic_melody(note_sequence, melody)
    melody_sequence = [Note(elem.nameWithOctave, quarterLength=interval) if type(elem) is Note else Rest(quarterLength=interval) for elem in melody_sequence for i in np.arange(0.0, elem.quarterLength, interval)]
    
    new_melody_sequence = []
    elem = None
    bar_length = 0.0

    # Handle notes in the melody due to bars and time signature
    def add_to_melody_sequence(new_melody_sequence, elem, bar_length):
        if type(elem) not in [Note, Rest]:
            pass
        elif bar_length + elem.quarterLength >= time_signature:
            extra = bar_length + elem.quarterLength - time_signature
            elem.quarterLength = time_signature - bar_length
            new_melody_sequence += [elem]
            bar_length = extra
            # The possible extra note
            if extra > 0.0:
                elem = Note(elem.nameWithOctave) if type(elem) is Note else Rest()
                elem.quarterLength = extra
        else:
            new_melody_sequence += [elem]
            bar_length += elem.quarterLength
            elem = None
        return (new_melody_sequence, elem, bar_length)
    
    for index, rhythm in enumerate(rhythm_sequence):
        if rhythm == 'Hold' and type(elem) is Note:
            elem.quarterLength += interval
        elif rhythm == 'Note':
            new_melody_sequence, elem, bar_length = add_to_melody_sequence(new_melody_sequence, elem, bar_length)
            elem = melody_sequence[index]
            elem.quarterLength = interval  
        elif rhythm == 'Rest' and type(elem) is Rest:
            elem.quarterLength += interval
        elif rhythm == 'Rest':
            new_melody_sequence, elem, bar_length = add_to_melody_sequence(new_melody_sequence, elem, bar_length)
            elem = Rest()
            elem.quarterLength = interval
    new_melody_sequence, elem, bar_length = add_to_melody_sequence(new_melody_sequence, elem, bar_length)
    return new_melody_sequence