from music21 import converter
from music21.note import *
from collections import Iterable
from music21.meter import TimeSignature
from music21.stream import Measure
from music21 import lily
import json

# Imports .mid to music21 song
def import_mid(filename):
    print('Start parsing...')
    song = converter.parse(filename)
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
        
# Some LilyPond files won't populate the measures/bars
# If this is the case, populate them
def populate_measures(song):
    # Initial values
    time_signature_length = 0
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
        if type(item) is TimeSignature:
            # Time signature
            time_signature_length = item.beatDuration.quarterLength * item.numerator
        elif type(item) is Note:
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
def equalise_interval(melody, interval):    
    def parse_elem(elem):
        return ([elem] + [Hold() for i in np.arange(interval, elem.quarterLength, interval)] if type(elem) is not Rest else
                [Rest(interval) for i in np.arange(0.0, elem.quarterLength, interval)])    
    
    return [e for elem in melody for e in parse_elem(elem)]
    
# Flattens a song into melodies, and then time interval equalises them
def flatten_equalised_parts(song, interval=0.0625):
    # Only look at notes, chords, and rests (not e.g. time signature, key signature, page layouts)
    parts = [[[elem for elem in bar if type(elem) in [Note, Chord, Rest]] for bar in part.getElementsByClass('Measure')] for part in song.getElementsByClass('Part')]
    
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
