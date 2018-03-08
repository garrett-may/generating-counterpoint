import random

# Builds a cumulative distribution for a list of probabilities
def _cumulative_distribution(probs):
    states = sorted(probs, key=lambda pair: pair[1])
    cumulative_dist = []
    summed = 0.0
    for elem,prob in states:
        summed += prob
        cumulative_dist += [(elem,summed)]
    if summed > 0.0:
        for index, (elem, prob) in enumerate(cumulative_dist):
            cumulative_dist[index] = (elem, prob / summed)
    return cumulative_dist    

# Returns the maximum probability from a list of probabilities
def max_probability(probs):
    (max_tr_prob, c_1) = (-1.0, None)
    for chord_1, tr_prob in probs:
        if tr_prob > max_tr_prob:
            (max_tr_prob, c_1) = (tr_prob, chord_1)
    return (c_1, max_tr_prob)
    
# Retuns a random probability from a list of probabilities
# The mapping allows transformations to the list, so that a greater chance
# of selecting a large probability can be made e.g. by squaring
def rand_probability(probs, mapping=lambda prob: prob):
    probs = [(elem, mapping(prob)) for elem, prob in probs]
    cumulative_dist = _cumulative_distribution(probs)
    r = random.random()
    for (elem, prob) in cumulative_dist:
        if prob >= r:
            return (elem, prob)
    else:
        return cumulative_dist[-1]
        
# Does the Viterbi backtrace algorithm to find the best sequence    
def max_backtrace(V, debug=False):
    opt = []                            
    
    # Find the max probability for the last state
    max_prob = max(value["prob"] for value in V[-1].values())
    
    prev = None
    # Find the state with the max probability
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt = [st]
            prev = st
            break
            
    # Follow the backtrace until we reach the start
    for t in range(len(V) - 2, -1, -1):
        opt = [V[t+1][prev]["prev"]] + opt
        prev = V[t+1][prev]["prev"]

    if debug:
        print('States: ' + ' '.join(opt) + ' | Probability: {}'.format(max_prob))
        
    return opt