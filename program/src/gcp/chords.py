from gcp import util, transform, corpus, viterbi

# General probability information
chords_unigrams = transform.import_JSON('json/chords_unigrams.json')
chords_bigrams = transform.import_JSON('json/chords_bigrams.json')
chords_trigrams = transform.import_JSON('json/chords_trigrams.json')
chords_tetragrams = transform.import_JSON('json/chords_tetragrams.json')
chords_given = transform.import_JSON('json/chords_given.json') # Note probabilites per chord
    
# Major probability information
chords_major_unigrams = transform.import_JSON('json/chords_major_unigrams.json')
chords_major_bigrams = transform.import_JSON('json/chords_major_bigrams.json')
chords_major_trigrams = transform.import_JSON('json/chords_major_trigrams.json')
chords_major_tetragrams = transform.import_JSON('json/chords_major_tetragrams.json')
chords_major_given = transform.import_JSON('json/chords_major_given.json')

# Minor probability information
chords_minor_unigrams = transform.import_JSON('json/chords_minor_unigrams.json')    
chords_minor_bigrams = transform.import_JSON('json/chords_minor_bigrams.json')
chords_minor_trigrams = transform.import_JSON('json/chords_minor_trigrams.json')
chords_minor_tetragrams = transform.import_JSON('json/chords_minor_tetragrams.json')
chords_minor_given = transform.import_JSON('json/chords_minor_given.json')

# Populates chord frequencies for a song
def populate_chords(song):
    # Initial information
    chord_types = util.chord_names
    note_types = util.note_names    
    
    unigrams = {chord_1:0 for chord_1 in chord_types}
    bigrams = {chord_1:{chord_2:0 for chord_2 in chord_types} for chord_1 in chord_types}
    trigrams = {chord_1:{chord_2:{chord_3:0 for chord_3 in chord_types} for chord_2 in chord_types} for chord_1 in chord_types}
    tetragrams = {chord_1:{chord_2:{chord_3:{chord_4:0 for chord_4 in chord_types} for chord_3 in chord_types} for chord_2 in chord_types} for chord_1 in chord_types}
    given = {chord_1:{note_1:0 for note_1 in note_types} for chord_1 in chord_types}

    # Get the key
    key = song.analyze('key')    

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key) for chord in chords]
    
    # Chord unigrams
    for i in range(0, len(chord_names)):
        unigrams[chord_names[i]] += 1

    # Chord bigrams
    for i in range(0, len(chord_names) - 1):
        bigrams[chord_names[i]][chord_names[i+1]] += 1

    # Chord trigrams
    for i in range(0, len(chord_names) - 2):
        trigrams[chord_names[i]][chord_names[i+1]][chord_names[i+2]] += 1
        
    # Chord tetragrams
    for i in range(0, len(chord_names) - 3):
        tetragrams[chord_names[i]][chord_names[i+1]][chord_names[i+2]][chord_names[i+3]] += 1
        
    # Note probabilities per chord   
    for chord_name, note_names in zip(chord_names, note_names_list):
        for note_name in note_names:
            given[chord_name][note_name] += 1

    return (unigrams, bigrams, trigrams, tetragrams, given)

# Builds the probabilties by reading from a particular corpus
def read_chords_corpus(corp, debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))

    # All
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_chords, filt=None, debug=debug)
   
    transform.export_JSON('json/chords_unigrams.json', unigrams)
    transform.export_JSON('json/chords_bigrams.json', bigrams)
    transform.export_JSON('json/chords_trigrams.json', trigrams)
    transform.export_JSON('json/chords_tetragrams.json', tetragrams)
    transform.export_JSON('json/chords_given.json', given)

    # Major
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_chords, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/chords_major_unigrams.json', unigrams)
    transform.export_JSON('json/chords_major_bigrams.json', bigrams)
    transform.export_JSON('json/chords_major_trigrams.json', trigrams)
    transform.export_JSON('json/chords_major_tetragrams.json', tetragrams)
    transform.export_JSON('json/chords_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_chords, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/chords_minor_unigrams.json', unigrams)
    transform.export_JSON('json/chords_minor_bigrams.json', bigrams)
    transform.export_JSON('json/chords_minor_trigrams.json', trigrams)
    transform.export_JSON('json/chords_minor_tetragrams.json', tetragrams)
    transform.export_JSON('json/chords_minor_given.json', given)
 
# Runs the algorithm to produce a chord sequence 
def algorithm(melody, debug=False):
    is_major = util.is_major(util.key(melody))
    if is_major:
        unigrams = chords_major_unigrams
        bigrams = chords_major_bigrams
        trigrams = chords_major_trigrams
        tetragrams = chords_major_tetragrams
        given = chords_major_given
    else:
        unigrams = chords_minor_unigrams
        bigrams = chords_minor_bigrams
        trigrams = chords_minor_trigrams
        tetragrams = chords_minor_tetragrams
        given = chords_minor_given
    
    transposed_melody = util.notes_names([note for note in melody], util.key(melody))
    
    # Viterbi algorithm
    chord_types = util.chord_names
    
    # Unigrams
    V = [{}]
    for chord_1 in chord_types:
        V[0][chord_1] = {'prob': unigrams[chord_1] * given[chord_1][transposed_melody[0]], 'prev': None}
    
    # Bigrams
    V.append({})
    for chord_2 in chord_types:
        tr_probs = [(chord_1, V[0][chord_1]['prob'] * bigrams[chord_1][chord_2]) for chord_1 in chord_types]
        (c_1, max_tr_prob) = viterbi.max_probability(tr_probs)
        V[1][chord_2] = {'prob': max_tr_prob * given[chord_2][transposed_melody[1]], 'prev': c_1}
        
    # Trigrams
    V.append({})
    for chord_3 in chord_types:
        tr_probs = [(chord_2, V[1][chord_2]['prob'] * trigrams[chord_1][chord_2][chord_3]) for chord_1 in chord_types for chord_2 in chord_types]
        (c_2, max_tr_prob) = viterbi.max_probability(tr_probs)
        V[2][chord_3] = {'prob': max_tr_prob * given[chord_3][transposed_melody[2]], 'prev': c_2}    
                        
    # Tetragrams                        
    for t in range(3, len(transposed_melody)):
        V.append({})
        for chord_4 in chord_types:
            tr_probs = [(chord_3, V[t-1][chord_3]['prob'] * tetragrams[chord_1][chord_2][chord_3][chord_4]) for chord_1 in chord_types for chord_2 in chord_types for chord_3 in chord_types]
            (c_3, max_tr_prob) = viterbi.max_probability(tr_probs)
            V[t][chord_4] = {'prob': max_tr_prob * given[chord_4][transposed_melody[t]], 'prev': c_3}
            
    return viterbi.max_backtrace(V, debug=debug)