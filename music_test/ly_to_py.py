import sys
from music21 import *
from music21.stream import *
from music21.meter import *
from music21.note import *
from music21.note import *
from music21.key import *
from music21.chord import *
import copy
import numpy as np
from numpy import prod
from hmmlearn import hmm
from collections import *
import json
from pprint import pprint
import random
from deap import base
from deap import creator
from deap import tools

#environment.set('musicxmlPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#environment.set('midiPath', '/mnt/c/Users/garrett-may/Desktop/music_test')

filename = sys.argv[1]  #sys.argv[1]

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_types = ['major', 'minor']
roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

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

song = import_mid(filename)    
song = populate_measures(song)

obs = [note.name for bar in song.elements for note in bar if type(note) is Note]      
        
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
            
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    #for line in dptable(V):
    #    print line
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
    return opt

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

#b = corpus.parse('bwv66.6')

#populate_chord_freq(b, unigrams, bigrams)

#for path in corpus.getComposer('bach'):
#    print('Parsing {} ...'.format(path))
#    work = corpus.parse(path)
#    populate_chord_freq(work, unigrams, bigrams)

#print_unigrams(unigrams)
#rint_bigrams(bigrams)

#js = json.dumps(unigrams)
#with open('unigrams.json', 'w') as fp:
#    fp.write(js)

#js = json.dumps(bigrams)
#with open('bigrams.json', 'w') as fp:
#    fp.write(js)

with open('unigrams.json', 'r') as fp:
    unigrams = json.load(fp)
with open('bigrams.json', 'r') as fp:
    bigrams = json.load(fp)  
    
states = [chord for chord,freq in unigrams.iteritems()]
    
start_p = {}
total = float(sum([freq for chord,freq in unigrams.iteritems()]))
for chord,freq in unigrams.iteritems():
    start_p[chord] = freq / total
    
trans_p = defaultdict(dict) 
for chord_1,next_chords in bigrams.iteritems():
    total = float(sum([freq for chord_2,freq in next_chords.iteritems()]))
    for chord_2,freq in next_chords.iteritems():
        trans_p[chord_1][chord_2] = freq / total
for chord_1 in states:
    for chord_2 in states:
        trans_p[chord_1][chord_2] = trans_p.get(chord_1, {}).get(chord_2, 0)
len_states = len(states)
for chord_1 in states:
    c_2_c_prob = trans_p[chord_1][chord_1]
    discount = 0 #0.1 #c_2_c_prob - 0.05
    trans_p[chord_1][chord_1] -= max(discount,0)
    for chord_2 in states:
        if chord_2 != chord_1:
            trans_p[chord_1][chord_2] += max(discount / (len_states - 1), 0)

emit_p = defaultdict(dict)
rotation_indices = [0, 2, 4, 5, 7, 9, 11]
key = song.analyze('Krumhansl')

def map_to_correct_pitch_name(pitch_name):
    alt_note_names = ['B#', 'D-', '?', 'E-', 'F-', 'E#', 'G-', '?', 'A-', '?', 'B-', 'C-']
    return note_names[alt_note_names.index(pitch_name)] if pitch_name in alt_note_names else pitch_name        

#def roman_to_pitch_names(roman, key):
#    chord = roman.RomanNumeral(roman, key)
#    pitch_names = [pitch.name for pitch in chord.pitches]

for state in states:
    chord = roman.RomanNumeral(state, key)
    #print('{}\n{}\n'.format(chord, chord.pitchNames))
    pitch_names = [pitch.name for pitch in chord.pitches]
    pitch_names = map(map_to_correct_pitch_name, pitch_names)
    is_major = chord.quality == 'major'
    is_minor = chord.quality == 'minor'
    pitch_values = [major_profile[0], major_profile[4], major_profile[7]] if is_major else \
                    [minor_profile[0], minor_profile[3], minor_profile[7]] if is_minor else \
                    []
    for note_name in note_names:        
        emit_p[state][note_name] = pitch_values[pitch_names.index(note_name)] / sum(pitch_values) if note_name in pitch_names and len(pitch_values) > 0 else 0
        # Because it's zero, e.g. A can't appear in G major chord
        
        #emit_p[state][note_name] = 1.0 / len(pitch_names) if note_name in pitch_names else 0
    
    #values = map(lambda num: num.lower() == state.lower().replace('-', '').replace('#', ''), roman_numerals)
    #numeral_index = values.index(True)
    #rotation_index = rotation_indices[numeral_index]
    #is_major = roman_numerals[numeral_index] == state.replace('-', '').replace('#', '')
    #profile = major_profile if is_major else minor_profile
    #total = sum(profile)
    #print('rotation_index:{}'.format(rotation_index))
    #for note,freq in zip(note_names, rotate(profile, rotation_index)):
    #    emit_p[state][note] = freq / total

opt = viterbi(obs, states, start_p, trans_p, emit_p)        
opt_deque = deque(opt)      

bars_with_chords = []
for bar in song.elements:
    bar_with_chords = []
    for note in bar:
        if type(note) == Note:
            bar_with_chords += [opt_deque.popleft()]    
    bars_with_chords += [bar_with_chords]
for bar_with_chords in bars_with_chords:
    print('Bar')
    for chord in bar_with_chords:
        print('{}:{}'.format(chord, roman.RomanNumeral(chord, key).pitches))

def fitness(chords, hmm_chords):
    summed = 0
    for index in range(0, len(chords)):
        #print('-#{}'.format(index))
        chord = chords[index]
        hmm_chord = hmm_chords[index]
        chord = roman.RomanNumeral(chord, Key('C'))
        hmm_chord = roman.RomanNumeral(hmm_chord, Key('C'))
        chord_pitches = map(map_to_correct_pitch_name, [pitch.name for pitch in chord.pitches])
        hmm_chord_pitches  = map(map_to_correct_pitch_name, [pitch.name for pitch in chord.pitches])
        dist = (note_names.index(chord_pitches[0]) - note_names.index(hmm_chord_pitches[0])) % octave
        summed += dist
    return summed

def individual(chord_types, length):
    chords = []
    for i in range(0, length):
        r = random.randint(0, len(chord_types) - 1)
        chords += [chord_types[r]]
    return chords

def mutate(chords, chance_of_mutation, chord_types):
    for i in range(0, len(chords)):
        r = random.uniform(0, 1)
        if r < chance_of_mutation:
            chords[i] = individual(chord_types, 1)[0]
    return chords

def child(father_chord, mother_chord):
    l = int(len(father_chord) / 2)
    return father_chord[:l] + mother_chord[l:]

def population(chord_types, length, num):
    return [individual(chord_types, length) for i in range(0, num)]

def genetic_algorithm(population, hmm_chords, chord_types, prop_of_best=0.2, chance_of_mutation=0.1):
    # Find the best
    #print('Find the best')
    population = sorted(population, key=lambda chords: fitness(chords, hmm_chords))
    #print('Keep the best')
    # Keep the best
    l = int(len(population) * prop_of_best)
    best = population[:l]

    # Breed to get the rest. Also apply mutation
    children = []
    for index in range(l, len(population)):
        r = random.randint(0, l - 1)
        s = r
        while s == r:
            #print('while')
            s = random.randint(0, l - 1)
        c = child(best[r], best[s])
        c = mutate(c, chance_of_mutation, chord_types)
        children += [c]

    return best + children

melody = [note for bar in song.elements for note in bar if type(note) == Note]
#pop = population(states, len(melody), 10)
#for i in range(0, 100):
#    print('#{}'.format(i))
#    pop = genetic_algorithm(pop, opt, states)
#for chords in pop:
#    print(chords)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def cumulative_distribution(chord_types):
    states = [(chord,prob) for chord,prob in chord_types.iteritems()]
    states = sorted(states, key=lambda (chord,prob): prob, reverse=True)
    cumulative_dist = []
    summed = 0.0
    for chord,prob in states:
        summed += prob
        cumulative_dist += [(chord,summed)]
    return cumulative_dist

cumulative_dist = cumulative_distribution(unigrams)

def attr_bool(cumulative_dist):
    r = random.random()
    for (chord,prob) in cumulative_dist:
        if prob >= r:
            return chord
    return cumulative_dist[-1][0]

def evaluate(individual):
    #a = 1
    #a_s = prod([emit_p[individual[index]][melody[index].name] for index in range(0, len(individual))])
    #b = 0
    #b_s = prod([trans_p[individual[index]][individual[index+1]] for index in range(0, len(individual) - 1)])
    #return (a * a_s + b * b_s,)
    return (sum([int(chord == 'I') for chord in individual]),)

def mutate(cumulative_dist, individual, indpb):
    for i in range(0, len(individual)):
        if random.random() < indpb:
            individual[i] = attr_bool(cumulative_dist)
    return (individual,)

toolbox = base.Toolbox()
toolbox.register("attr_bool", attr_bool, cumulative_dist)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, len(melody))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate, cumulative_dist, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = toolbox.population(n=10)
CXPB, MUTPB = 0.5, 0.2
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
fits = [ind.fitness.values[0] for ind in pop]

g = 0
while max(fits) < 100 and g < 1:
    g += 1
    offspring = toolbox.select(pop, len(pop))
    offsprint = list(map(toolbox.clone, offspring))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind,fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    pop[:] = offspring
    best_ind = tools.selBest(pop, len(pop))
    #best_chord = [roman.romanNumeralFromChord(Chord([int(n) for n in c]), Key('C')).romanNumeral for c in best_ind]
    print("Gen #{}: best individual is {}".format(g, best_ind))

#pprint(emit_p)
        
#print_unigrams(start_p)
#print_bigrams(trans_p)
#print_bigrams(emit_p)
#print(trans_p['I']['vi'])

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
