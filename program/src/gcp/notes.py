from gcp import util, transform, corpus, viterbi

# General probability information
notes_unigrams = transform.import_JSON('json/notes_unigrams.json')
notes_bigrams = transform.import_JSON('json/notes_bigrams.json')
notes_trigrams = transform.import_JSON('json/notes_trigrams.json')
notes_tetragrams = transform.import_JSON('json/notes_tetragrams.json')
notes_given = transform.import_JSON('json/notes_given.json') # Chord probabilites per note
notes_2_given = transform.import_JSON('json/notes_2_given.json') # Note probabilities per note

# General probability information including note octaves
notes_with_octaves_unigrams = transform.import_JSON('json/notes_with_octaves_unigrams.json')
notes_with_octaves_bigrams = transform.import_JSON('json/notes_with_octaves_bigrams.json')
notes_with_octaves_given = transform.import_JSON('json/notes_with_octaves_given.json')

# Major probability information
notes_major_unigrams = transform.import_JSON('json/notes_major_unigrams.json')
notes_major_bigrams = transform.import_JSON('json/notes_major_bigrams.json')
notes_major_trigrams = transform.import_JSON('json/notes_major_trigrams.json')
notes_major_tetragrams = transform.import_JSON('json/notes_major_tetragrams.json')
notes_major_given = transform.import_JSON('json/notes_major_given.json')
notes_2_major_given = transform.import_JSON('json/notes_2_major_given.json')

# Major probability information including note octaves
notes_with_octaves_major_unigrams = transform.import_JSON('json/notes_with_octaves_major_unigrams.json')
notes_with_octaves_major_bigrams = transform.import_JSON('json/notes_with_octaves_major_bigrams.json')
notes_with_octaves_major_given = transform.import_JSON('json/notes_with_octaves_major_given.json')

# Minor probability information
notes_minor_unigrams = transform.import_JSON('json/notes_minor_unigrams.json')
notes_minor_bigrams = transform.import_JSON('json/notes_minor_bigrams.json')
notes_minor_trigrams = transform.import_JSON('json/notes_minor_trigrams.json')
notes_minor_tetragrams = transform.import_JSON('json/notes_minor_tetragrams.json')
notes_minor_given = transform.import_JSON('json/notes_minor_given.json')
notes_2_minor_given = transform.import_JSON('json/notes_2_minor_given.json')

# Minor probability information including note octaves
notes_with_octaves_minor_unigrams = transform.import_JSON('json/notes_with_octaves_minor_unigrams.json')
notes_with_octaves_minor_bigrams = transform.import_JSON('json/notes_with_octaves_minor_bigrams.json')
notes_with_octaves_minor_given = transform.import_JSON('json/notes_with_octaves_minor_given.json')

# Populates note frequencies for a song
def populate_notes(song):
    # Initial information
    note_types = util.note_names #[note_name + str(octave) for note_name in util.note_names for octave in range(0, 8)]
    chord_types = util.chord_names
    
    unigrams = {note_1:0 for note_1 in note_types}
    bigrams = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    trigrams = {note_1:{note_2:{note_3:0 for note_3 in note_types} for note_2 in note_types} for note_1 in note_types}
    tetragrams = {note_1:{note_2:{note_3:{note_4:0 for note_4 in note_types} for note_3 in note_types} for note_2 in note_types} for note_1 in note_types}
    given = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key, include_octave=False) for chord in chords]
    
    part_names = [util.notes_names(part.flat.getElementsByClass('Note'), key, include_octave=False) for part in song.getElementsByClass('Part')]        
    for note_names in part_names:    
        # Note unigrams
        for i in range(0, len(note_names)):
            unigrams[note_names[i]] += 1

        # Note bigrams
        for i in range(0, len(note_names) - 1):
            bigrams[note_names[i]][note_names[i+1]] += 1

        # Note trigrams
        for i in range(0, len(note_names) - 2):
            trigrams[note_names[i]][note_names[i+1]][note_names[i+2]] += 1
            
        # Note tetragrams
        for i in range(0, len(note_names) - 3):
            tetragrams[note_names[i]][note_names[i+1]][note_names[i+2]][note_names[i+3]] += 1
        
     # Note probabilities per note    
    for chord_name, note_names in zip(chord_names, note_names_list):
        for i in range(0, len(note_names) - 1):
            given[note_names[i+1]][note_names[i]] += 1

    return (unigrams, bigrams, trigrams, tetragrams, given)
    
# Populates note frequencies for a song
def populate_notes_per_chord(song):
    # Initial information
    note_types = util.note_names #[note_name + str(octave) for note_name in util.note_names for octave in range(0, 8)]
    chord_types = util.chord_names
    
    unigrams = {}
    bigrams = {}
    trigrams = {}
    tetragrams = {}
    given = {note_1:{chord_1:0 for chord_1 in chord_types} for note_1 in note_types}    
    
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key, include_octave=False) for chord in chords]

    # Chord probabilities per note    
    for chord_name, note_names in zip(chord_names, note_names_list):
        for note_name in note_names:
            given[note_name][chord_name] += 1

    return (unigrams, bigrams, trigrams, tetragrams, given)
    
# Populates note frequencies for a song
def populate_notes_with_octaves(song):
    # Initial information
    note_types = [note_name + str(octave) for note_name in util.note_names for octave in range(0, 8)]
    chord_types = util.chord_names
    
    unigrams = {note_1:0 for note_1 in note_types}
    bigrams = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    trigrams = {}
    tetragrams = {}
    given = {note_1:{note_2:0 for note_2 in note_types} for note_1 in note_types}
    
    # Get the key
    key = song.analyze('key')

    # Apply the naive chord algorithm
    chords_naive = song.chordify()
    
    chords = chords_naive.flat.getElementsByClass('Chord')
    chord_names = [util.roman(chord, key) for chord in chords]
    note_names_list = [util.notes_names(chord, key, include_octave=True) for chord in chords]
    
    part_names = [util.notes_names(part.flat.getElementsByClass('Note'), key, include_octave=True) for part in song.getElementsByClass('Part')]        
    for note_names in part_names:    
        # Note unigrams
        for i in range(0, len(note_names)):
            unigrams[note_names[i]] += 1
            
        # Note bigrams
        for i in range(0, len(note_names) - 1):
            bigrams[note_names[i]][note_names[i+1]] += 1
            
    # Note probabilities per note    
    for chord_name, note_names in zip(chord_names, note_names_list):
        for i in range(0, len(note_names) - 1):
            given[note_names[i+1]][note_names[i]] += 1
            
    return (unigrams, bigrams, trigrams, tetragrams, given)

# Builds the probabilties by reading from a particular corpus
def read_notes_corpus(corp, debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))
    
    # All
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes, filt=None, debug=debug)
   
    transform.export_JSON('json/notes_unigrams.json', unigrams)
    transform.export_JSON('json/notes_bigrams.json', bigrams)
    transform.export_JSON('json/notes_trigrams.json', trigrams)
    transform.export_JSON('json/notes_tetragrams.json', tetragrams)
    transform.export_JSON('json/notes_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_major_unigrams.json', unigrams)
    transform.export_JSON('json/notes_major_bigrams.json', bigrams)
    transform.export_JSON('json/notes_major_trigrams.json', trigrams)
    transform.export_JSON('json/notes_major_tetragrams.json', tetragrams)
    transform.export_JSON('json/notes_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_minor_unigrams.json', unigrams)
    transform.export_JSON('json/notes_minor_bigrams.json', bigrams)
    transform.export_JSON('json/notes_minor_trigrams.json', trigrams)
    transform.export_JSON('json/notes_minor_tetragrams.json', tetragrams)
    transform.export_JSON('json/notes_minor_given.json', given)
    
    ###################
    
    # All
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes_per_chord, filt=None, debug=debug)
   
    transform.export_JSON('json/notes_2_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes_per_chord, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_2_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes_per_chord, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_2_minor_given.json', given)
    
    ###################
    
    # All
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes_with_octaves, filt=None, debug=debug)
   
    transform.export_JSON('json/notes_with_octaves_unigrams.json', unigrams)
    transform.export_JSON('json/notes_with_octaves_bigrams.json', bigrams)
    transform.export_JSON('json/notes_with_octaves_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes_with_octaves, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_with_octaves_major_unigrams.json', unigrams)
    transform.export_JSON('json/notes_with_octaves_major_bigrams.json', bigrams)
    transform.export_JSON('json/notes_with_octaves_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, tetragrams, given) = corpus.read_corpus(corp, populate_notes_with_octaves, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_with_octaves_minor_unigrams.json', unigrams)
    transform.export_JSON('json/notes_with_octaves_minor_bigrams.json', bigrams)
    transform.export_JSON('json/notes_with_octaves_minor_given.json', given)
   
# Runs the algorithm to produce a note sequence 
def algorithm(melody, chords, debug=False):
    is_major = util.is_major(util.key(melody))
    if is_major:
        unigrams = notes_major_unigrams
        bigrams = notes_major_bigrams
        trigrams = notes_major_trigrams
        tetragrams = notes_major_tetragrams
        given = notes_major_given
        given_2 = notes_2_major_given
        
        with_octaves_unigrams = notes_with_octaves_major_unigrams
        with_octaves_bigrams = notes_with_octaves_major_bigrams
        with_octaves_given = notes_with_octaves_major_given
    else:
        unigrams = notes_minor_unigrams
        bigrams = notes_minor_bigrams
        trigrams = notes_minor_trigrams
        tetragrams = notes_minor_tetragrams
        given = notes_minor_given
        given_2 = notes_2_minor_given
        
        with_octaves_unigrams = notes_with_octaves_minor_unigrams
        with_octaves_bigrams = notes_with_octaves_minor_bigrams
        with_octaves_given = notes_with_octaves_minor_given
                                            
    def square(prob):
        return prob*prob
        
    transposed_melody = util.notes_names([note for note in melody], util.key(melody))
                                            
    # Viterbi algorithm (adapted for randomness)
    note_types = util.note_names
    
    # Unigrams
    V = [{}]
    for note_1 in note_types:
        V[0][note_1] = {'prob': unigrams[note_1] * (given[note_1][transposed_melody[0]]) * given_2[note_1][chords[0]], 'prev': None}
    
    # Bigrams
    V.append({})
    for note_2 in note_types:
        tr_probs = [(note_1, V[0][note_1]['prob'] * bigrams[note_1][note_2]) for note_1 in note_types]
        (n_1, max_tr_prob) = viterbi.rand_probability(tr_probs, mapping=square)
        V[1][note_2] = {'prob': max_tr_prob * (given[note_2][transposed_melody[1]]) * given_2[note_2][chords[1]], 'prev': n_1}
    
    # Trigrams
    V.append({})
    for note_3 in note_types:
        tr_probs = [(note_2, V[1][note_2]['prob'] * trigrams[note_1][note_2][note_3]) for note_1 in note_types for note_2 in note_types]        
        (n_2, max_tr_prob) = viterbi.rand_probability(tr_probs, mapping=square)
        V[2][note_3] = {'prob': max_tr_prob * (given[note_3][transposed_melody[2]]) * given_2[note_3][chords[2]], 'prev': n_2}    
    
    # Tetragrams    
    for t in range(3, len(chords)):
        V.append({})
        for note_4 in note_types:
            tr_probs = [(note_3, V[t-1][note_3]['prob'] * tetragrams[note_1][note_2][note_3][note_4]) for note_1 in note_types for note_2 in note_types for note_3 in note_types]
            (n_3, max_tr_prob) = viterbi.rand_probability(tr_probs, mapping=square) if t != len(chords) - 1 else viterbi.max_probability(tr_probs)
            V[t][note_4] = {'prob': max_tr_prob * (given[note_4][transposed_melody[t]]) * given_2[note_4][chords[t]], 'prev': n_3}
          
    mel = viterbi.max_backtrace(V, debug=debug)    
        
    # Viterbi algorithm (for octaves)      
    
    # Unigrams
    V = [{}]
    for note_1 in [mel[0] + str(octave) for octave in range(0, 8)]:
        V[0][note_1] = {'prob': with_octaves_unigrams[note_1], 'prev': None}   
        #V[0][note_1] = {'prob': with_octaves_unigrams[note_1] * (with_octaves_given[note_1][transposed_melody[0].nameWithOctave] + with_octaves_given[transposed_melody[0].nameWithOctave][note_1]), 'prev': None}   

    # Bigrams
    for t in range(1, len(mel)):
        V.append({})
        for note_2 in [mel[t] + str(octave) for octave in range(0, 8)]:
            tr_probs = [(note_1, V[t-1][note_1]['prob'] * with_octaves_bigrams[note_1][note_2]) for note_1 in V[t-1].keys()]
            (n_1, max_tr_prob) = viterbi.max_probability(tr_probs)
            V[t][note_2] = {'prob': max_tr_prob, 'prev': n_1}
            #V[t][note_2] = {'prob': max_tr_prob * (with_octaves_given[note_1][transposed_melody[t].nameWithOctave] + with_octaves_given[transposed_melody[t].nameWithOctave][note_1]), 'prev': n_1}
          
          
    return viterbi.max_backtrace(V, debug=debug)