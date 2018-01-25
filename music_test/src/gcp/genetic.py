from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
from gcp import util
from numpy import prod
import numpy

melody = []

def cumulative_distribution(chord_types):
    states = [(chord,prob) for chord,prob in chord_types.items()]
    states = sorted(states, key=lambda pair: pair[1], reverse=True)
    cumulative_dist = []
    summed = 0.0
    for chord,prob in states:
        summed += prob
        cumulative_dist += [(chord,summed)]
    return cumulative_dist

def attr_float(cumulative_dist):
    r = random.random()
    for (chord,prob) in cumulative_dist:
        if prob >= r:
            return chord
    return cumulative_dist[-1][0]

def evaluate(individual):
    if individual == []:
        return 0.0
    prob = 1.0
    for index, chord_1 in enumerate(individual):
        if index == 0:
            prob *= util.chord_unigrams[individual[index]]
        #elif index == 1:
        else:
            prob *= util.chord_bigrams[individual[index-1]][individual[index]]
        #else:
        #    prob *= util.chord_trigrams[individual[index-2]][individual[index-1]][individual[index]]
        prob *= util.chord_given[individual[index]][melody[index].name]
    return (prob,)
    
    #a = 1
    #a_s = sum([util.note_prob[individual[index]][melody[index].name] for index in range(0, len(individual))])
    #b = 1
    #b_s = sum([util.bigrams[individual[index]][individual[index+1]] for index in range(0, len(individual) - 1)])
    #c = 0
    #c_s = sum([util.trigrams[individual[index]][individual[index+1]][individual[index+2]] for index in range(0, len(individual) - 2)])
    #return (a * a_s + b * b_s + c * c_s,)
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
    
def algorithm(mel):
    global melody
    melody = mel
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    cumulative_dist = cumulative_distribution(util.chord_unigrams)

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
    return [chord for chord in best_ind[0]]