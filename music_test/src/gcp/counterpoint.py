from music21.corpus import getComposer
from gcp import corpus
from gcp import transform
from gcp import util

def read_notes_corpus(corp, debug=False):
    def is_major(song):
        return util.is_major(song.analyze('key'))

    # All
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(corp, corpus.populate_notes, filt=None, debug=debug)
   
    transform.export_JSON('json/notes_unigrams.json', unigrams)
    transform.export_JSON('json/notes_bigrams.json', bigrams)
    transform.export_JSON('json/notes_trigrams.json', trigrams)
    transform.export_JSON('json/notes_given.json', given)
        
    # Major
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(corp, corpus.populate_notes, filt=lambda song: is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_major_unigrams.json', unigrams)
    transform.export_JSON('json/notes_major_bigrams.json', bigrams)
    transform.export_JSON('json/notes_major_trigrams.json', trigrams)
    transform.export_JSON('json/notes_major_given.json', given)

    # Minor
    (unigrams, bigrams, trigrams, given) = corpus.read_corpus(corp, corpus.populate_notes, filt=lambda song: not is_major(song), debug=debug)
   
    transform.export_JSON('json/notes_minor_unigrams.json', unigrams)
    transform.export_JSON('json/notes_minor_bigrams.json', bigrams)
    transform.export_JSON('json/notes_minor_trigrams.json', trigrams)
    transform.export_JSON('json/notes_minor_given.json', given)
   
def algorithm(chords, algorithm):
    (unigrams, bigrams, trigrams, given) = (util.notes_unigrams, util.notes_bigrams, util.notes_trigrams, util.notes_given)
    return algorithm.algorithm([note.nameWithOctave for note in chords], unigrams, bigrams, trigrams, given, rand=True)