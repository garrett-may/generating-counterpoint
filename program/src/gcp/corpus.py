from music21 import corpus

# Total sum of the values of a dictionary
def _total(item):
    return sum(_total(i) for i in item.values()) if type(item) is dict else item
    
# Converts frequency to probability (total sum will be 1.0)
def _freq_to_prob(item, total):
    return {key: _freq_to_prob(value, total) for key, value in item.items()} if type(item) is dict else item / total if total > 0.0 else 0.0
    
# Converts the information's frequency to probability
def _convert_frequency_to_probability(information):
    (unigrams, bigrams, trigrams, tetragrams, given) = information
    unigrams = _freq_to_prob(unigrams, float(_total(unigrams)))
    bigrams = _freq_to_prob(bigrams, float(_total(bigrams)))
    trigrams = _freq_to_prob(trigrams, float(_total(trigrams)))
    tetragrams = _freq_to_prob(tetragrams, float(_total(tetragrams)))
    given = {key: _freq_to_prob(values, float(_total(values))) for key, values in given.items()}
    return (unigrams, bigrams, trigrams, tetragrams, given)
    
# Merges two dictionaries together by summing the values of keys
def _merge_dictionaries(this, that):
    if this == {}:
        return that
    elif that == {}:
        return this
    elif type(this) is dict and type(that) is dict:
        return {key: _merge_dictionaries(this[key], that[key]) for key in set(this.keys()) | set(that.keys())}
    else:
        return this + that
        
# Merges the information together        
def _merge(x, y):
    (a0, b0, c0, d0, e0) = x
    (a1, b1, c1, d1, e1) = y
    return (_merge_dictionaries(a0, a1),
            _merge_dictionaries(b0, b1),
            _merge_dictionaries(c0, c1),
            _merge_dictionaries(d0, d1),
            _merge_dictionaries(e0, e1))
    
# Reads a corpus, from a particular composer, using a particular populator function
def read_corpus(corp, populate, filt=None, debug=False):
    information = ({}, {}, {}, {}, {})
    for path in corp:
        if debug:
            print('Parsing {} ...'.format(path))
        song = corpus.parse(path)
        if filt != None and not filt(song):
            continue
        information = _merge(information, populate(song))
    return _convert_frequency_to_probability(information)
            