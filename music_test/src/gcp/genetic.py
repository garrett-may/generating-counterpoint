from deap import base, creator, tools, algorithms
import random
import numpy

# Creates the cumulative distribution of the unigrams
def _cumulative_distribution(unigrams):
    states = sorted(unigrams.items(), key=lambda pair: pair[1], reverse=True)
    cumulative_dist = []
    summed = 0.0
    for elem,prob in states:
        summed += prob
        cumulative_dist += [(elem,summed)]
    return cumulative_dist

# Chooses a random element from the cumulative distribution
def _attr_float(cumulative_dist):
    r = random.random()
    for (elem,prob) in cumulative_dist:
        if prob >= r:
            return elem
    return cumulative_dist[-1][0]

# Evaluates the sequence
def evaluate(sequence, unigrams, bigrams, given, individual):
    if individual == []:
        return 0.0
    prob = 1.0
    for index, chord_1 in enumerate(individual):
        if index == 0:
            prob *= unigrams[individual[index]]
        else:
            prob *= bigrams[individual[index-1]][individual[index]]
        prob *= given[individual[index]][sequence[index]]
    return (prob,)

# Mutates the sequence
def _mutate(cumulative_dist, individual, indpb):
    for i in range(0, len(individual)):
        if random.random() < indpb:
            individual[i] = _attr_float(cumulative_dist)
    return (individual,)    
    
# Algorithm
def algorithm(sequence, unigrams, bigrams, given, evaluate=evaluate):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    cumulative_dist = _cumulative_distribution(unigrams)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", _attr_float, cumulative_dist)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, len(sequence))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, sequence, unigrams, bigrams, given)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", _mutate, cumulative_dist, indpb=0.2)
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