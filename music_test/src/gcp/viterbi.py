from gcp import util
import random

# Apply the Viterbi algorithm to find the most probable sequence
def _viterbi(obs, states, start_p, trans_p, emit_p, evaluate=None):   
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Evaluate the current state
    if evaluate != None:
        V = evaluate(V, 0)
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
        # Evaluate the current state
        if evaluate != None:
            V = evaluate(V, t)
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

    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of '.format(max_prob))
    return opt
    
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

def max_probability(probs):
    (max_tr_prob, c_1) = (-1.0, None)
    for chord_1, tr_prob in probs:
        if tr_prob > max_tr_prob:
            (max_tr_prob, c_1) = (tr_prob, chord_1)
    return (c_1, max_tr_prob)
    
def rand_probability(probs):
    probs = [(elem, prob*prob) for elem, prob in probs]
    cumulative_dist = _cumulative_distribution(probs)
    r = random.random()
    for (elem, prob) in cumulative_dist:
        if prob >= r:
            return (elem, prob)
    else:
        return cumulative_dist[-1]
    
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
    
def _viterbi_2(obs, chord_types, unigrams, bigrams, trigrams, tetragrams, given, evaluate=None, rand=False):
    V = [{}]
    for chord_1 in chord_types:
        V[0][chord_1] = {'prob': unigrams[chord_1] * given[chord_1][obs[0]], 'prev': None}
    
    V.append({})
    for chord_2 in chord_types:
        tr_probs = [(chord_1, V[0][chord_1]['prob'] * bigrams[chord_1][chord_2]) for chord_1 in chord_types]
        (c_1, max_tr_prob) = _max_prob(tr_probs)
        V[1][chord_2] = {'prob': max_tr_prob * given[chord_2][obs[1]], 'prev': c_1}
        
    V.append({})
    for chord_3 in chord_types:
        tr_probs = [(chord_2, V[1][chord_2]['prob'] * trigrams[chord_1][chord_2][chord_3]) for chord_1 in chord_types for chord_2 in chord_types]
        
        if not rand:                
            (c_2, max_tr_prob) = _max_prob(tr_probs)
        else:
            tr_probs = [(chord_2, prob*prob) for chord_2, prob in tr_probs]
            cumulative_dist = _cumulative_distribution(tr_probs)
            r = random.random()
            for (elem,prob) in cumulative_dist:
                if prob >= r:
                    (c_2, max_tr_prob) = (elem, prob)
                    break
            else:
                (c_2, max_tr_prob) = cumulative_dist[-1]
        V[2][chord_3] = {'prob': max_tr_prob * given[chord_3][obs[2]], 'prev': c_2}    
                        
    for t in range(3, len(obs)):
        V.append({})
        for chord_4 in chord_types:
            tr_probs = [(chord_3, V[t-1][chord_3]['prob'] * tetragrams[chord_1][chord_2][chord_3][chord_4]) for chord_1 in chord_types for chord_2 in chord_types for chord_3 in chord_types]
            
            if not rand:                
                (c_3, max_tr_prob) = _max_prob(tr_probs)
            else:
                tr_probs = [(chord_3, prob*prob) for chord_3, prob in tr_probs]
                cumulative_dist = _cumulative_distribution(tr_probs)
                r = random.random()
                for (elem,prob) in cumulative_dist:
                    if prob >= r:
                        (c_3, max_tr_prob) = (elem, prob)
                        break
                else:
                    (c_3, max_tr_prob) = cumulative_dist[-1]
            V[t][chord_4] = {'prob': max_tr_prob * given[chord_4][obs[t]], 'prev': c_3}
          
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

    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of '.format(max_prob))
    return opt
    
# Algorithm
def algorithm(sequence, unigrams, bigrams, trigrams, tetragrams, given, evaluate=None, rand=False):
    if trigrams == None:
        return _viterbi(sequence, [elem for elem in unigrams.keys()], unigrams, bigrams, given, evaluate)
    else:
        return _viterbi_2(sequence, [elem for elem in unigrams.keys()], unigrams, bigrams, trigrams, tetragrams, given, evaluate, rand)
    