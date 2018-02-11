from gcp import util

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

    
    
def _viterbi_2(obs, chord_types, unigrams, bigrams, trigrams, given, evaluate=None):
    V= [{}]
    for chord_1 in chord_types:
        V[0][chord_1] = {'prob': unigrams[chord_1] * given[chord_1][obs[0]], 'prev': None}
    t = 1
    #for t in range(1, len(obs)):
    V.append({})
    for chord_2 in chord_types:
        (max_tr_prob, c_1) = (-1.0, None)
        for chord_1 in chord_types:
            tr_prob = V[t-1][chord_1]['prob'] * bigrams[chord_1][chord_2]
            if tr_prob > max_tr_prob:
                (max_tr_prob, c_1) = (tr_prob, chord_1)
        V[t][chord_2] = {'prob': max_tr_prob * given[chord_2][obs[t]], 'prev': c_1}
                        
    for t in range(2, len(obs)):
        V.append({})
        for chord_3 in chord_types:
            (max_tr_prob, c_2) = (-1.0, None)
            for chord_1 in chord_types:
                for chord_2 in chord_types:
                    tr_prob = V[t-1][chord_2]['prob'] * trigrams[chord_1][chord_2][chord_3]
                    #tr_prob = V[t-2][chord_1]['prob'] * V[t-1][chord_2]['prob'] * bigrams[chord_2][chord_3]
                    if tr_prob > max_tr_prob:
                        (max_tr_prob, c_2) = (tr_prob, chord_2)
            V[t][chord_3] = {'prob': max_tr_prob * given[chord_3][obs[t]], 'prev': c_2}
            
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
def algorithm(sequence, unigrams, bigrams, trigrams, given, evaluate=None):
    if trigrams == None:
        return _viterbi(sequence, [elem for elem in unigrams.keys()], unigrams, bigrams, given, evaluate)
    else:
        return _viterbi_2(sequence, [elem for elem in unigrams.keys()], unigrams, bigrams, trigrams, given, evaluate)
    