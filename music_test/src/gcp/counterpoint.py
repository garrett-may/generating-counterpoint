from gcp import corpus
from gcp import transform

def read_notes_corpus(composer='bach', debug=False):
    # Major
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_notes, is_major=True, debug=debug)
   
    transform.export_JSON('json/notes_major_unigrams.json', unigrams)
    transform.export_JSON('json/notes_major_bigrams.json', bigrams)
    transform.export_JSON('json/notes_major_trigrams.json', trigrams)
    transform.export_JSON('json/notes_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_notes, is_major=False, debug=debug)
   
    transform.export_JSON('json/notes_minor_unigrams.json', unigrams)
    transform.export_JSON('json/notes_minor_bigrams.json', bigrams)
    transform.export_JSON('json/notes_minor_trigrams.json', trigrams)
    transform.export_JSON('json/notes_minor_given.json', given)
   
def algorithm(chords, algorithm):
    (unigrams, bigrams, trigrams, given) = (util.notes_unigrams, util.notes_bigrams, util.notes_trigrams, util.notes_given)
    return algorithm.algorithm(chords, unigrams, bigrams, given)