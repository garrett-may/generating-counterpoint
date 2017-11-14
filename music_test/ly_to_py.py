import sys
from music21 import *
from music21.stream import *
from music21.meter import *
from music21.note import *
from music21.note import *
import copy
import numpy as np
from numpy import prod
from hmmlearn import hmm
from collections import Iterable

#environment.set('musicxmlPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#environment.set('midiPath', '/mnt/c/Users/garrett-may/Desktop/music_test')

filename = sys.argv[1]  #sys.argv[1]

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_types = ['major', 'minor']

octave = 12
chromatic_scale = range(0, octave)
    
circle_of_fifths = [note * 7 % octave for note in chromatic_scale]

major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

def rotate(l, n):
    return l[-n:] + l[:-n]

def import_mid(filename):
    print('Start parsing...')
    song = converter.parse(filename)
    print('End parsing')
    return song
    
def export_ly(song, filename):
    lpc = lily.translate.LilypondConverter()
    lpMusicList = lily.lilyObjects.LyMusicList()
    lpc.context = lpMusicList
    lpc.appendObjectsToContextFromStream(song)
    
    with open(filename + '.ly', 'w') as file:
        file.write(str(lpc.context))
    
def populate_measures(song):
    time_signature_length = 0
    seen_length = 0
    bars = []
    current_bar = []
    
    def append_bar(current_bar, seen_length, item):
        current_bar += [item]
        seen_length += item.duration.quarterLength
        return (current_bar, seen_length)
    
    def check_bar(bars, current_bar, seen_length):
        if seen_length >= time_signature_length:
            bars += [current_bar]
            current_bar = []
            seen_length = 0
        return (bars, current_bar, seen_length)
    
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
        
    part = find_bars(song)
    for item in part:
        #print(item)
        if type(item) is TimeSignature:
            time_signature_length = item.beatDuration.quarterLength * item.numerator
            #print('TS: {}'.format(time_signature_length))
        elif type(item) is Note:
            #print(str(item.name) + " | " + str(item.octave) + " | " + str(item.duration.type))
            (current_bar, seen_length) = append_bar(current_bar, seen_length, item)
            (bars, current_bar, seen_length) = check_bar(bars, current_bar, seen_length)
        elif type(item) is Rest:
            #print('rest')
            (current_bar, seen_length) = append_bar(current_bar, seen_length, item)
            (bars, current_bar, seen_length) = check_bar(bars, current_bar, seen_length)
            
    # LilyPond might forget a rest at the end
    if time_signature_length - seen_length > 0:
        (current_bar, seen_length) = append_bar(current_bar, seen_length, Rest(quarterLength = time_signature_length - seen_length))
    (bars, current_bar, seen_length) = check_bar(bars, current_bar, seen_length)
                
    song.elements = []
    for bar in bars:
        #print('Bar')
        measure = Measure()
        for n in bar:
            measure.append(copy.deepcopy(n))
            #print(str(n.name) + " | " + str(n.duration.type))
        song.append(measure)
    return song
    
def generate_chords(song):        
        
    for bar in song.elements:
        chord_prob = [0] * 12
        b = [note for note in bar if type(note) is Note]
        note_durations = [note.duration.quarterLength for note in b]
        note_pitches = [int(note.pitch.ps % 12) for note in b]
        for j in range(0, 12):
            profile = rotate(major_profile, j)
            note_prob = [1] * 12
            for i in range(0, len(note_pitches)):
                note_pitch = note_pitches[i]
                fifth_diff = abs(circle_of_fifths[j] - circle_of_fifths[note_pitch]) % octave
                note_prob[note_pitch] = note_durations[i] * profile[note_pitch] * (octave - fifth_diff)
                #note_prob[note_pitch] = fifth_diff
            sum_prob = prod(note_prob)
            chord_prob[j] += sum_prob
            
        profile = rotate(major_profile, 0)
        best_chord = [(note_names[i], chord_prob[i]) for i in range(0, len(chord_prob))]
        best_chord = sorted(best_chord, key=lambda tp: tp[1], reverse=True)
        #chord_prob = [chord_prob[i] * profile[i] for i in range(0, len(chord_prob))]
        print('Best chord: {}'.format(best_chord))
            
def generate_key_naive(song):
    def coefficient(x, y, i):           
        #x_m = sum(x) / 12.0        
        #y_m = sum(y) / 12.0
        x = rotate(x, i)
        y = rotate(y, i)
        num = sum([(x[i]) * (y[i]) for i in chromatic_scale])
        den = (sum([(xi) ** 2 for xi in x]) * sum([(yi) ** 2 for yi in y])) ** 0.5
        return num / den
    
    notes = [note for bar in song.elements for note in bar if type(note) is Note]
    profile_types = [major_profile, minor_profile]
    y = [sum(map(lambda n: n.duration.quarterLength, filter(lambda n: (n.pitch.ps % octave) == p, notes))) for p in chromatic_scale]
    coefficients = [coefficient(x, y, p) for x in profile_types for p in chromatic_scale]
    coefficients = [(note_names[i % octave], key_types[i / octave]) for (i,r) in enumerate(coefficients)]
    return sorted(coefficients, key=lambda r: r[1])[0]
    
def generate_key_Krumhansl(song):
    
    def coefficient(x, y, i):           
        x_m = sum(x) / 12.0        
        y_m = sum(y) / 12.0
        x = rotate(x, i)
        y = rotate(y, i)
        num = sum([(x[i] - x_m) * (y[i] - y_m) for i in chromatic_scale])
        den = (sum([(xi - x_m) ** 2 for xi in x]) * sum([(yi - y_m) ** 2 for yi in y])) ** 0.5
        return num / den
    
    notes = [note for bar in song.elements for note in bar if type(note) is Note]
    profile_types = [major_profile, minor_profile]
    y = [sum(map(lambda n: n.duration.quarterLength, filter(lambda n: (n.pitch.ps % octave) == p, notes))) for p in chromatic_scale]
    coefficients = [coefficient(x, y, p) for x in profile_types for p in chromatic_scale]
    coefficients = [(note_names[i % octave], key_types[i / octave]) for (i,r) in enumerate(coefficients)]
    return sorted(coefficients, key=lambda r: r[1])[0]
    
            
song = import_mid(filename)    
song = populate_measures(song)

#print(song.elements)      
        
key = song.analyze('Krumhansl')
print(key.tonic.name, key.mode)
key = generate_key_Krumhansl(song)
print(key)

generate_chords(song)
#print(circle_of_fifths)
    
export_ly(song, filename)
    
#key = b.analyze('KrumhanslSchmuckler')   
#print('Bar key: {} | {}'.format(key.tonic.name, key.mode))
#for k in key.alternateInterpretations:
#    print('- {}'.format(k))
                
#chordTypes = [('C', 'major'), ('G', 'major'), ('D', 'major')]        
#model = hmm.GaussianHMM(n_components=len(chordTypes), covariance_type="full")
#model.fit([map(lambda x: x.pitch.ps, filter(lambda x: type(x) == note.Note, bars))])

#logprob, state = model.decode(bars, algorithm="viterbi")
#print("States: {}".format(",".join(map(lambda x: chordTypes[x], state))))

#song.show('midi')

#with open(filename, "r") as file:	
	#lines = file.readlines()	
	#lines = [line.replace('\n', '').replace('\r', '') for line in lines]
	#for line in lines:
	#	print(line)
	#str = ''.join(lines)
	#parser = abjad.lilypondparsertools.LilyPondParser('nederlands')
	#parser = abjad.lilypondparsertools.LilyPondParser('nederlands')
	#container = parser(str)
	#print(container)
	#abjad.show(container) 
	#container = lilypondparsertools.parse_reduced_ly_syntax(str)
	#print(container)