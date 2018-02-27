from music21.corpus import getComposer
from gcp import corpus
from gcp import transform
from gcp import util
from gcp import viterbi

notes_with_octaves_unigrams = transform.import_JSON('json/notes_with_octaves_unigrams.json')
notes_with_octaves_bigrams = transform.import_JSON('json/notes_with_octaves_bigrams.json')
notes_with_octaves_given = transform.import_JSON('json/notes_with_octaves_given.json')


notes_unigrams = transform.import_JSON('json/notes_unigrams.json')
notes_bigrams = transform.import_JSON('json/notes_bigrams.json')
notes_trigrams = transform.import_JSON('json/notes_trigrams.json')
notes_tetragrams = transform.import_JSON('json/notes_tetragrams.json')
notes_given = transform.import_JSON('json/notes_given.json') # Chord probabilites per note
notes_2_given = transform.import_JSON('json/notes_2_given.json') # Note probabilities per note

notes_with_octaves_major_unigrams = transform.import_JSON('json/notes_with_octaves_major_unigrams.json')
notes_with_octaves_major_bigrams = transform.import_JSON('json/notes_with_octaves_major_bigrams.json')
notes_with_octaves_major_given = transform.import_JSON('json/notes_with_octaves_major_given.json')

notes_major_unigrams = transform.import_JSON('json/notes_major_unigrams.json')
notes_major_bigrams = transform.import_JSON('json/notes_major_bigrams.json')
notes_major_trigrams = transform.import_JSON('json/notes_major_trigrams.json')
notes_major_tetragrams = transform.import_JSON('json/notes_major_tetragrams.json')
notes_major_given = transform.import_JSON('json/notes_major_given.json')
notes_2_major_given = transform.import_JSON('json/notes_2_major_given.json')

notes_with_octaves_minor_unigrams = transform.import_JSON('json/notes_with_octaves_minor_unigrams.json')
notes_with_octaves_minor_bigrams = transform.import_JSON('json/notes_with_octaves_minor_bigrams.json')
notes_with_octaves_minor_given = transform.import_JSON('json/notes_with_octaves_minor_given.json')

notes_minor_unigrams = transform.import_JSON('json/notes_minor_unigrams.json')
notes_minor_bigrams = transform.import_JSON('json/notes_minor_bigrams.json')
notes_minor_trigrams = transform.import_JSON('json/notes_minor_trigrams.json')
notes_minor_tetragrams = transform.import_JSON('json/notes_minor_tetragrams.json')
notes_minor_given = transform.import_JSON('json/notes_minor_given.json')
notes_2_minor_given = transform.import_JSON('json/notes_2_minor_given.json')

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
        
        #if len(note_names) > 1:
        #    for note_name in note_names[1:]:
        #        given[note_name][note_names[0]] += 1
            
    return (unigrams, bigrams, trigrams, tetragrams, given)

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

def read_notes_corpus(corp, debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))
        
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
        
    ###################
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
   
def algorithm(melody, chords):
    is_major = True
    (unigrams, bigrams, trigrams, tetragrams, given) = (notes_major_unigrams, notes_major_bigrams,  
                                            notes_major_trigrams, notes_major_tetragrams, notes_major_given) if is_major else \
                                            (notes_minor_unigrams, notes_minor_bigrams,
                                            notes_minor_trigrams, notes_minor_tetragrams, notes_minor_given)
                                            
    given_2 = notes_2_major_given if is_major else notes_2_minor_given
                                            
    (with_octaves_unigrams, with_octaves_bigrams, with_octaves_given) = (notes_with_octaves_major_unigrams, notes_with_octaves_major_bigrams,                                      notes_with_octaves_major_given) if is_major else \
                                        (notes_with_octaves_minor_unigrams, notes_with_octaves_minor_bigrams, notes_with_octaves_minor_given)
                                            
    # Viterbi algorithm (adapted for randomness)                                         
    #obs = chords
    note_types = util.note_names
    
    # Unigrams
    V = [{}]
    for note_1 in note_types:
        V[0][note_1] = {'prob': unigrams[note_1] * (given[note_1][melody[0].name]) * given_2[note_1][chords[0]], 'prev': None}
    
    # Bigrams
    V.append({})
    for note_2 in note_types:
        tr_probs = [(note_1, V[0][note_1]['prob'] * bigrams[note_1][note_2]) for note_1 in note_types]
        (n_1, max_tr_prob) = viterbi.rand_probability(tr_probs)
        V[1][note_2] = {'prob': max_tr_prob * (given[note_1][melody[1].name]) * given_2[note_1][chords[1]], 'prev': n_1}
    
    # Trigrams
    V.append({})
    for note_3 in note_types:
        tr_probs = [(note_2, V[1][note_2]['prob'] * trigrams[note_1][note_2][note_3]) for note_1 in note_types for note_2 in note_types]        
        (n_2, max_tr_prob) = viterbi.rand_probability(tr_probs)
        V[2][note_3] = {'prob': max_tr_prob * (given[note_1][melody[2].name]) * given_2[note_1][chords[2]], 'prev': n_2}    
    
    # Tetragrams    
    for t in range(3, len(chords)):
        V.append({})
        for note_4 in note_types:
            tr_probs = [(note_3, V[t-1][note_3]['prob'] * tetragrams[note_1][note_2][note_3][note_4]) for note_1 in note_types for note_2 in note_types for note_3 in note_types]
            (n_3, max_tr_prob) = viterbi.rand_probability(tr_probs) if t != len(chords) - 1 else viterbi.max_probability(tr_probs)
            V[t][note_4] = {'prob': max_tr_prob * (given[note_1][melody[t].name]) * given_2[note_1][chords[t]], 'prev': n_3}
          
    mel = viterbi.max_backtrace(V, debug=True)    
    # Viterbi algorithm      
    
    # Unigrams
    V = [{}]
    for note_1 in [mel[0] + str(octave) for octave in range(0, 8)]:
        V[0][note_1] = {'prob': with_octaves_unigrams[note_1], 'prev': None}   
        #V[0][note_1] = {'prob': with_octaves_unigrams[note_1] * (with_octaves_given[note_1][melody[0].nameWithOctave] + with_octaves_given[melody[0].nameWithOctave][note_1]), 'prev': None}   

    # Bigrams
    for t in range(1, len(mel)):
        V.append({})
        for note_2 in [mel[t] + str(octave) for octave in range(0, 8)]:
            tr_probs = [(note_1, V[t-1][note_1]['prob'] * with_octaves_bigrams[note_1][note_2]) for note_1 in V[t-1].keys()]
            (n_1, max_tr_prob) = viterbi.max_probability(tr_probs)
            V[t][note_2] = {'prob': max_tr_prob, 'prev': n_1}
            #V[t][note_2] = {'prob': max_tr_prob * (with_octaves_given[note_1][melody[t].nameWithOctave] + with_octaves_given[melody[t].nameWithOctave][note_1]), 'prev': n_1}
          
          
    return viterbi.max_backtrace(V, debug=True)                                          
                                            
    #return algorithm.algorithm([note.nameWithOctave for note in chords], unigrams, bigrams, trigrams, tetragrams, given, rand=True)