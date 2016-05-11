# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

def create_ngrams(sequence, n):
    """Create ngrams from sequence, e.g. ([1,2,3], 2) -> [(1,2), (2,3)]
       Note that fewer sequence items than n results in an empty list being returned"""
    # credit: http://stackoverflow.com/questions/2380394/simple-implementation-of-n-gram-tf-idf-and-cosine-similarity-in-python
    sequence = list(sequence)
    count = max(0, len(sequence) - n + 1)
    bigrams = [tuple(sequence[i:i+n]) for i in range(count)]
    return bigrams

def bigrams_dissimilarity(question_words, sentence_words):
    """Bigram distance metric, term frequency is ignored,
       0 if bigrams are identical, 1.0 if no bigrams are common"""
    terms1 = set(create_ngrams(question_words, 2)) # was using nltk.bigrams
    terms2 = set(create_ngrams(sentence_words, 2))
    shared_terms = terms1.intersection(terms2)
    all_terms = terms1.union(terms2)
    dist = 1.0
    if len(all_terms) > 0:
        dist = 1.0 - (len(shared_terms) / float(len(all_terms)))
    return dist


def bigram_features(question_words, sentence_words):
    """Bigram distance metric, term frequency is ignored,
       0 if bigrams are identical, 1.0 if no bigrams are common"""
    terms1 = set(create_ngrams(question_words, 2)) # was using nltk.bigrams
    terms2 = set(create_ngrams(sentence_words, 2))
    shared_terms = terms1.intersection(terms2)
    all_terms = terms1.union(terms2)
    dist = 1.0
    match = len(shared_terms)
    if len(all_terms) > 0:
        dist = 1.0 - (len(shared_terms) / float(len(all_terms)))
    return {'dissimilarity': dist, 'match': match}
