from music21.note import Note, Rest
from gcp import util, transform, corpus, viterbi
from gcp.transform import Hold
    
# General probability information
rhythms_unigrams = transform.import_JSON('json/rhythms_unigrams.json')
rhythms_bigrams = transform.import_JSON('json/rhythms_bigrams.json')
rhythms_trigrams = transform.import_JSON('json/rhythms_trigrams.json')
rhythms_tetragrams = transform.import_JSON('json/rhythms_tetragrams.json')
rhythms_given = transform.import_JSON('json/rhythms_given.json') # Rhythm probabilites per rhythm
    
# Major probability information
rhythms_major_unigrams = transform.import_JSON('json/rhythms_major_unigrams.json')
rhythms_major_bigrams = transform.import_JSON('json/rhythms_major_bigrams.json')
rhythms_major_trigrams = transform.import_JSON('json/rhythms_major_trigrams.json')
rhythms_major_tetragrams = transform.import_JSON('json/rhythms_major_tetragrams.json')
rhythms_major_given = transform.import_JSON('json/rhythms_major_given.json')

# Minor probability information
rhythms_minor_unigrams = transform.import_JSON('json/rhythms_minor_unigrams.json')    
rhythms_minor_bigrams = transform.import_JSON('json/rhythms_minor_bigrams.json')
rhythms_minor_trigrams = transform.import_JSON('json/rhythms_minor_trigrams.json')
rhythms_minor_tetragrams = transform.import_JSON('json/rhythms_minor_tetragrams.json')
rhythms_minor_given = transform.import_JSON('json/rhythms_minor_given.json')    
    
# Populates note frequencies for a song
def populate_rhythms(song):
    # Initial information
    rhythm_mapping = {Note: 'Note', Rest: 'Rest', Hold: 'Hold'}
    rhythm_types = rhythm_mapping.values()
    note_types = util.note_names
    chord_types = util.chord_names
    
    unigrams = {rhythm_1:0 for rhythm_1 in rhythm_types}
    bigrams = {rhythm_1:{rhythm_2:0 for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    trigrams = {rhythm_1:{rhythm_2:{rhythm_3:0 for rhythm_3 in rhythm_types} for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    tetragrams = {rhythm_1:{rhythm_2:{rhythm_3:{rhythm_4:0 for rhythm_4 in rhythm_types} for rhythm_3 in rhythm_types} for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    given = {rhythm_1:{rhythm_2:0 for rhythm_2 in rhythm_types} for rhythm_1 in rhythm_types}
    
    # Get the key
    key = [key for key in song.flat.getElementsByClass('Key')][0]

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key) for chord in chords]
    
    parts = transform.flatten_equalised_parts(song)
    parts = [[elem for ls in part for elem in ls] for part in parts]
    
    for part in parts:
        part = [rhythm_mapping[type(elem)] for elem in part]
        
        # Rhythm unigrams
        for i in range(0, len(part)):
            unigrams[part[i]] += 1

        # Rhythm bigrams
        for i in range(0, len(part) - 1):
            bigrams[part[i]][part[i+1]] += 1

        # Rhythm trigrams
        for i in range(0, len(part) - 2):
            trigrams[part[i]][part[i+1]][part[i+2]] += 1
            
        # Rhythm tetragrams
        for i in range(0, len(part) - 3):
            tetragrams[part[i]][part[i+1]][part[i+2]][part[i+3]] += 1
    
    # Rhythm probabilites per rhythm
    for i in range(len(parts[0])):
        elems = [part[i] for part in parts]
        for i in range(0, len(elems) - 1):
            rhythm_1 = rhythm_mapping[type(elems[i])]
            rhythm_2 = rhythm_mapping[type(elems[i+1])]
            given[rhythm_2][rhythm_1] += 1       
            
    return (unigrams, bigrams, trigrams, tetragrams, given)
    
# Builds the probabilties by reading from a particular corpus
def read_rhythms_corpus(corp, debug=False):
    def is_major(song):
        return util.is_major([key for key in song.flat.getElementsByClass('Key')][0])

    # All
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_rhythms, filt=None, debug=debug)
   
    transform.export_JSON('json/rhythms_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_tetragrams.json', tetragrams)
    transform.export_JSON('json/rhythms_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_rhythms, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/rhythms_major_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_major_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_major_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_major_tetragrams.json', tetragrams)
    transform.export_JSON('json/rhythms_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_rhythms, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/rhythms_minor_unigrams.json', unigrams)
    transform.export_JSON('json/rhythms_minor_bigrams.json', bigrams)
    transform.export_JSON('json/rhythms_minor_trigrams.json', trigrams)
    transform.export_JSON('json/rhythms_minor_tetragrams.json', tetragrams)
    transform.export_JSON('json/rhythms_minor_given.json', given)
    
# Runs the algorithm to produce a rhythm sequence 
def algorithm(melody, debug=False):
    is_major = util.is_major(util.key(melody))
    if is_major:
        unigrams = rhythms_major_unigrams
        bigrams = rhythms_major_bigrams
        trigrams = rhythms_major_trigrams
        tetragrams = rhythms_major_tetragrams
        given = rhythms_major_given
    else:
        unigrams = rhythms_minor_unigrams
        bigrams = rhythms_minor_bigrams
        trigrams = rhythms_minor_trigrams
        tetragrams = rhythms_minor_tetragrams
        given = rhythms_minor_given
    
    part = transform.equalise_interval(melody)
    rhythm_mapping = {Note: 'Note', Rest: 'Rest', Hold: 'Hold'}
    rhythm = [rhythm_mapping[type(elem)] for elem in part]
    
    # Viterbi algorithm (adapted for randomness)      
    rhythm_types = rhythm_mapping.values()
    
    # Unigrams
    V = [{}]
    for rhythm_1 in rhythm_types:
        V[0][rhythm_1] = {'prob': unigrams[rhythm_1] * given[rhythm_1][rhythm[0]], 'prev': None}
    
    # Bigrams
    V.append({})
    for rhythm_2 in rhythm_types:
        tr_probs = [(rhythm_1, V[0][rhythm_1]['prob'] * bigrams[rhythm_1][rhythm_2]) for rhythm_1 in rhythm_types]
        (r_1, max_tr_prob) = viterbi.rand_probability(tr_probs)
        V[1][rhythm_2] = {'prob': max_tr_prob * given[rhythm_2][rhythm[1]], 'prev': r_1}
    
    # Trigrams
    V.append({})
    for rhythm_3 in rhythm_types:
        tr_probs = [(rhythm_2, V[1][rhythm_2]['prob'] * trigrams[rhythm_1][rhythm_2][rhythm_3]) for rhythm_1 in rhythm_types for rhythm_2 in rhythm_types]        
        (r_2, max_tr_prob) = viterbi.rand_probability(tr_probs)
        V[2][rhythm_3] = {'prob': max_tr_prob * given[rhythm_3][rhythm[2]], 'prev': r_2}    
    
    # Tetragrams    
    for t in range(3, len(rhythm)):
        V.append({})
        for rhythm_4 in rhythm_types:
            tr_probs = [(rhythm_3, V[t-1][rhythm_3]['prob'] * tetragrams[rhythm_1][rhythm_2][rhythm_3][rhythm_4]) for rhythm_1 in rhythm_types for rhythm_2 in rhythm_types for rhythm_3 in rhythm_types]
            (r_3, max_tr_prob) = viterbi.rand_probability(tr_probs)
            V[t][rhythm_4] = {'prob': max_tr_prob * given[rhythm_4][rhythm[t]], 'prev': r_3}
          
    return viterbi.max_backtrace(V, debug=debug)