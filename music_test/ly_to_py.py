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
from collections import *
import json

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

def circle_of_fifths_diff(a, b):
    diff = abs(circle_of_fifths[a] - circle_of_fifths[b])
    return min(diff, octave - diff)
    
def generate_chords(song):        
    major_heuristic = [0,5,4,5,1,4,6,1,5,4,2,4]
    best_chords = []
    for bar in song.elements:
        chord_prob = [0] * 12
        b = [note for note in bar if type(note) is Note]
        note_durations = [note.duration.quarterLength for note in b]
        note_pitches = [int(note.pitch.ps % 12) for note in b]
        for j in range(0, 12):
            profile = rotate(major_profile, j)
            heuristic = rotate(major_heuristic, j)
            note_prob = [1] * 12
            for i in range(0, len(note_pitches)):
                note_pitch = note_pitches[i]
                #fifth_diff = abs(circle_of_fifths[j] - circle_of_fifths[note_pitch]) % octave
                note_prob[note_pitch] = heuristic[note_pitch]
                #note_prob[note_pitch] = note_durations[i] * profile[note_pitch] * (octave - fifth_diff)
                #note_prob[note_pitch] = fifth_diff
            fifth_diff = circle_of_fifths_diff(note_names.index(best_chords[-1][0][0]), j) if len(best_chords) > 0 else 0
            sum_prob = sum(note_prob) + fifth_diff # 0 is C major
            chord_prob[j] += sum_prob
            
        profile = rotate(major_profile, 0)
        best_chord = [(note_names[i], chord_prob[i]) for i in range(0, len(chord_prob))]
        best_chord = sorted(best_chord, key=lambda x: x[1])
        #best_chord = sorted(best_chord, key=lambda tp: tp[1], reverse=True)
        #chord_prob = [chord_prob[i] * profile[i] for i in range(0, len(chord_prob))]
        best_chords += [best_chord]
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

#song = import_mid(filename)    
#song = populate_measures(song)

#print(song.elements)      
        
#key = song.analyze('Krumhansl')
#print(key.tonic.name, key.mode)
#key = generate_key_Krumhansl(song)
#print(key)

#generate_chords(song)
#print(circle_of_fifths)
    
#export_ly(song, filename)

def populate_chord_freq(song, unigrams, bigrams):
    key = song.analyze('key')
    chords_naive = song.chordify()
    chord_names = [roman.romanNumeralFromChord(chord, key).romanNumeral for chord in chords_naive.flat.getElementsByClass('Chord')]
    for i in range(0, len(chord_names) - 1):
        # Unigrams
        unigrams[chord_names[i]] += 1

        # Bigrams
        next_chords = bigrams.get(chord_names[i], defaultdict(int))
        next_chords[chord_names[i+1]] += 1
        bigrams[chord_names[i]] = next_chords
    for i in range(len(chord_names) - 1, len(chord_names)):
        # Unigrams
        unigrams[chord_names[i]] += 1

def print_unigrams(unigrams):
    for chord,freq in unigrams.iteritems():
        print('[{}]:{}'.format(chord, freq))

def print_bigrams(bigrams):
    for chord_1,next_chords in bigrams.iteritems():
        for chord_2,freq in next_chords.iteritems():
            print('[{}][{}]:{}'.format(chord_1, chord_2, freq))

#b = corpus.parse('bwv66.6')

unigrams = defaultdict(int)
bigrams = defaultdict(dict)

#populate_chord_freq(b, unigrams, bigrams)

#for path in corpus.getComposer('bach'):
#    print('Parsing {} ...'.format(path))
#    work = corpus.parse(path)
#    populate_chord_freq(work, unigrams, bigrams)

#print_unigrams(unigrams)
print_bigrams(bigrams)

#js = json.dumps(unigrams)
#with open('unigrams.json', 'w') as fp:
#    fp.write(js)

#js = json.dumps(bigrams)
#with open('bigrams.json', 'w') as fp:
#    fp.write(js)

#with open('unigrams.json', 'r') as fp:
#    data = json.load(fp)
##total = float(sum([freq for chord,freq in data.iteritems()]))
#for chord,freq in data.iteritems():
#    data[chord] = 100 * freq / total
#print_unigrams(data)

with open('bigrams.json', 'r') as fp:
    bigrams = json.load(fp)
print_bigrams(bigrams)

#for chord in bChords.recurse().getElementsByClass('Chord'):
#    print(roman.romanNumeralFromChord(chord, key).romanNumeral)

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
