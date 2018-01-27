from gcp import corpus
from gcp import transform
from gcp import util

def read_chords_corpus(composer='bach', debug=False):
    # Major
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_chords, is_major=True, debug=debug)
   
    transform.export_JSON('json/chords_major_unigrams.json', unigrams)
    transform.export_JSON('json/chords_major_bigrams.json', bigrams)
    transform.export_JSON('json/chords_major_trigrams.json', trigrams)
    transform.export_JSON('json/chords_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_chords, is_major=False, debug=debug)
   
    transform.export_JSON('json/chords_minor_unigrams.json', unigrams)
    transform.export_JSON('json/chords_minor_bigrams.json', bigrams)
    transform.export_JSON('json/chords_minor_trigrams.json', trigrams)
    transform.export_JSON('json/chords_minor_given.json', given)
 
def algorithm(melody, algorithm):
    is_major = util.is_major(util.key(melody))
    (unigrams, bigrams, trigrams, given) = (util.chords_major_unigrams, util.chords_major_bigrams,  
                                            util.chords_major_trigrams, util.chords_major_given) if is_major else \
                                            (util.chords_minor_unigrams, util.chords_minor_bigrams,
                                            util.chords_minor_trigrams, util.chords_minor_given)
    return algorithm.algorithm([note.name for note in melody], unigrams, bigrams, given)