from music21.key import Key
from gcp import corpus
from gcp import transform
from gcp import util

def read_chords_corpus(composer='bach', debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))

    # All
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_chords, filter=None, debug=debug)
   
    transform.export_JSON('json/chords_unigrams.json', unigrams)
    transform.export_JSON('json/chords_bigrams.json', bigrams)
    transform.export_JSON('json/chords_trigrams.json', trigrams)
    transform.export_JSON('json/chords_given.json', given)

    # Major
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_chords, filter=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/chords_major_unigrams.json', unigrams)
    transform.export_JSON('json/chords_major_bigrams.json', bigrams)
    transform.export_JSON('json/chords_major_trigrams.json', trigrams)
    transform.export_JSON('json/chords_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(composer, corpus.populate_chords, filter=lambda song: not is_major(song), debug=debug)
   
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
    transposed_melody = util.notes_names([note.name for note in melody], util.key(melody))
    return algorithm.algorithm(transposed_melody, unigrams, bigrams, given)