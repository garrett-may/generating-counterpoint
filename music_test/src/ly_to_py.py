import sys
from music21 import *
from music21.stream import *
from music21.meter import *
from music21.note import *
from music21.note import *
from music21.key import *
from music21.chord import *
from music21.pitch import *
from music21.interval import *
import copy
import numpy as np
import numpy
from numpy import prod
from hmmlearn import hmm
from collections import *
from pprint import pprint

from gcp import util
from gcp import transform
from gcp import chords as chords
from gcp import counterpoint as counterpoint
from gcp import genetic
from gcp import viterbi
import json

#environment.set('musicxmlPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#environment.set('midiPath', '/mnt/c/Users/garrett-may/Desktop/music_test')

filename = sys.argv[1]  #sys.argv[1]

#with open('unigrams.json', 'r') as fp:
#    unigrams = json.load(fp)
    
# Bigrams
#with open('bigrams.json', 'r') as fp:
#    bigrams = json.load(fp)  
    
# Trigrams
#with open('trigrams.json', 'r') as fp:
#    trigrams = json.load(fp)
    
# Note probabilites per chord
#with open('note_prob.json', 'r') as fp:
#    note_prob = json.load(fp)
    
#print(sum([prob for chord_1,prob in util.unigrams.iteritems()]))
#print(sum([prob for chord_1,n_chords in util.bigrams.iteritems() for chord_2,prob in n_chords.iteritems()]))
#print(sum([prob for chord_1,n_chords in util.trigrams.iteritems() for chord_2,nn_chords in n_chords.iteritems() for chord_3,prob in nn_chords.iteritems()]))

#total_1 = sum([prob for chord_1,prob in unigrams.iteritems()])
#total_2 = sum([prob for chord_1,n_chords in bigrams.iteritems() for chord_2,prob in n_chords.iteritems()])
#total_3 = sum([prob for chord_1,n_chords in trigrams.iteritems() for chord_2,nn_chords in n_chords.iteritems() for chord_3,prob in nn_chords.iteritems()])

#unigrams, bigrams, trigrams, note_prob = counterpoint.read_notes_corpus()

#transform.export_JSON('json/note_unigrams.json', unigrams)
#transform.export_JSON('json/note_bigrams.json', bigrams)
#transform.export_JSON('json/note_trigrams.json', trigrams)
#transform.export_JSON('json/chord_note_prob.json', note_prob)


#for chord_1,freq in unigrams.iteritems():
#    a, b = int(round(freq)), int(round(total_1*util.unigrams[chord_1]))
#    print('{} {} {}'.format(a, b, a == b))
#for chord_1,n_chords in bigrams.iteritems():
#    for chord_2,freq in n_chords.iteritems():
#        a, b = int(round(freq)), int(round(total_2*util.bigrams[chord_1][chord_2]))
#        print('{} {} {}'.format(a, b, a == b))

song = transform.import_mid(filename)
transform.populate_measures(song)
melody = [note.name for bar in song.elements for note in bar if type(note) == Note]
chords = viterbi.algorithm_chords(melody)
viterbi.algorithm_melody(chords)


#genetic.algorithm(melody)


#song = import_mid(filename)    
#song = populate_measures(song)

#obs = [note.name for bar in song.elements for note in bar if type(note) is Note]      
        
#key = song.analyze('Krumhansl')
#print(key.tonic.name, key.mode)
#key = generate_key_Krumhansl(song)
#print(key)

#generate_chords(song)
#print(circle_of_fifths)
    
#export_ly(song, filename)


def print_unigrams(unigrams):
    for chord,freq in unigrams.iteritems():
        print('[{}]:{}'.format(chord, freq))

def print_bigrams(bigrams):
    for chord_1,next_chords in bigrams.iteritems():
        for chord_2,freq in next_chords.iteritems():
            print('[{}][{}]:{}'.format(chord_1, chord_2, freq))

#b = corpus.parse('bwv66.6')

#unigrams = {}
#bigrams = {}
#trigrams = {}

#populate_chord_freq(b, unigrams, bigrams, trigrams)

#for path in corpus.getComposer('bach'):
#    print('Parsing {} ...'.format(path))
#    work = corpus.parse(path)
#    populate_chord_freq(work, unigrams, bigrams, trigrams)

#print_unigrams(unigrams)
#rint_bigrams(bigrams)

#js = json.dumps(unigrams)
#with open('unigrams.json', 'w') as fp:
#    fp.write(js)

#js = json.dumps(bigrams)
#with open('bigrams.json', 'w') as fp:
#    fp.write(js)

#js = json.dumps(trigrams)
#with open('trigrams.json', 'w') as fp:
#    fp.write(js)

#with open('json/unigrams.json', 'r') as fp:
#    unigrams = json.load(fp)
#with open('json/bigrams.json', 'r') as fp:
#    bigrams = json.load(fp)  
#with open('json/trigrams.json', 'r') as fp:
#    trigrams = json.load(fp)
#with open('json/note_prob.json', 'r') as fp:
    #note_prob = json.load(fp)
    
#states = [chord for chord,freq in unigrams.iteritems()]    

#unigrams, bigrams, trigrams, note_prob = chords.read_chords_corpus()    

#js = json.dumps(unigrams)
#with open('json/unigrams.json', 'w') as fp:
#    fp.write(js)

#js = json.dumps(bigrams)
#with open('json/bigrams.json', 'w') as fp:
#    fp.write(js)

#js = json.dumps(trigrams)
#with open('json/trigrams.json', 'w') as fp:
#    fp.write(js)
    
#js = json.dumps(note_prob)
#with open('json/note_prob.json', 'w') as fp:
#    fp.write(js)
  
"""    
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
        
tri_p = defaultdict(lambda : defaultdict(dict))   
for chord_1, next_chords in trigrams.iteritems():
    total_1 = 0
    for chord_2, next_next_chords in next_chords.iteritems():
        for chord_3,freq in next_next_chords.iteritems():
            total_1 += freq
    for chord_2, next_next_chords in next_chords.iteritems():
        total_2 = 0
        for chord_3,freq in next_next_chords.iteritems():
            total_2 += freq
        for chord_3,freq in next_next_chords.iteritems():
            tri_p[chord_1][chord_2][chord_3] = (freq / float(total_1)) / float(total_2)

for chord_1 in states:
    for chord_2 in states:
        for chord_3 in states:
            tri_p[chord_1][chord_2][chord_3] = tri_p.get(chord_1, defaultdict(dict)).get(chord_2, defaultdict(int)).get(chord_3, 0)
        
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
"""

    
#def roman_to_pitch_names(roman, key):
#    chord = roman.RomanNumeral(roman, key)
#    pitch_names = [pitch.name for pitch in chord.pitches]
"""
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
"""

"""
emit_p = defaultdict(dict)
for state in states:
    total = sum([prob for note, prob in note_prob[state].iteritems()])
    for note in note_names:
        emit_p[state][note] = note_prob[state].get(note, 0) / float(total)
print_bigrams(emit_p)
    
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

cumulative_dist = cumulative_distribution(start_p)

def attr_float(cumulative_dist):
    r = random.random()
    for (chord,prob) in cumulative_dist:
        if prob >= r:
            return chord
    return cumulative_dist[-1][0]

def evaluate(individual):
    a = 1
    a_s = sum([emit_p[individual[index]][melody[index].name] for index in range(0, len(individual))])
    b = 1
    b_s = sum([trans_p[individual[index]][individual[index+1]] for index in range(0, len(individual) - 1)])
    c = 1
    c_s = sum([tri_p[individual[index]][individual[index+1]][individual[index+2]] for index in range(0, len(individual) - 2)])
    return (a * a_s + b * b_s + c * c_s,)
    #note_sum = 0
    #for index in range(0, len(individual)):
    #    note = melody[index]
    #    chord = individual[index]
    #    note_sum += emit_p[chord][note.name]
    #return (note_sum,)
    #return (sum([int(chord == 'I') for chord in individual]),)

def mutate(cumulative_dist, individual, indpb):
    for i in range(0, len(individual)):
        if random.random() < indpb:
            individual[i] = attr_float(cumulative_dist)
    return (individual,)

toolbox = base.Toolbox()
toolbox.register("attr_float", attr_float, cumulative_dist)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, len(melody))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate, cumulative_dist, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = toolbox.population(n=1000)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=1000, stats=stats, halloffame=hof, verbose=True)
best_ind = tools.selBest(pop, 1)
print("Gen #{}: best individual is:".format(1000))
for ind in best_ind:
    print(ind)

opt_deque = deque(best_ind[0])      

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

"""
"""
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
    """
"""
"""
"""
note_prob = defaultdict(dict)
for path in corpus.getComposer('bach'):
    print('Parsing {} ...'.format(path))
    work = corpus.parse(path)
    key = work.analyze('key')
    print('Key: {}'.format(key))
    #interval = Interval(key.tonic, Pitch('C'))
    interval = (note_names.index(map_to_correct_pitch_name(key.tonic.name)) - note_names.index('C')) % octave
    #work = work.transpose(interval)
    chords_naive = work.chordify()
    for chord in chords_naive.flat.getElementsByClass('Chord'):
        notes = [note.name for note in chord]
        notes = map(map_to_correct_pitch_name, notes)
        notes = map(lambda n: note_names[(note_names.index(map_to_correct_pitch_name(n)) - interval) % octave], notes)
        chord_name = roman.romanNumeralFromChord(chord, key).romanNumeral        
        #print('{}|{}'.format(chord_name, note_names))
        for note_name in notes:
            note_prob[chord_name] = note_prob.get(chord_name, defaultdict(int))
            note_prob[chord_name][note_name] += 1

#for state in states:
#    for note_name in note_names:
#        note_prob[state][note_name] = note_prob.get(state, {}).get(note_name, 0)

#for chord_name, notes in note_prob.iteritems():
#    for note_name, prob in notes.iteritems():
#        print('{}:{}:{}'.format(chord_name, note_name, prob))

js = json.dumps(note_prob)
with open('note_prob.json', 'w') as fp:
    fp.write(js)
    """
   
"""
    #chord_names = [roman.romanNumeralFromChord(chord, key).romanNumeral for chord in chords_naive.flat.getElementsByClass('Chord')]


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
"""