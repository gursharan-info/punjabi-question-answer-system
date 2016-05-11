# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import numpy as np
import math
from collections import Counter
import relationship_calulator as rc
import bonus
import nltk
from nltk.collocations import *
# Calculates CoGM (Center of Gravity Metric) value


lex_words = [
    'N_NN',
    'N_NNP',
    'V_VM',
    'V_VM_VNF',
    'V_VM_VINF',
    'V_VM_VNG',
    'V_VAUX',
    'JJ',
    'RB'
]

def calculate_a_pair(named_entities, named_entity_types, word_tags):
    ne_count = len(named_entities)
    if ne_count == 0:
        # nouns = [n for n in word_tags if n in ['N_NN','N_NNP']]
        nouns = [n for n in word_tags if n in ['N_NNP']]
        pair = {'X1': len(nouns), 'Y1': len(set(nouns))}
        # print pair
    else:
        pair = {'X1': len(named_entities), 'Y1': len(set(named_entity_types))}
        # print pair

    return pair

def ngrams(sequence, n):
    """Create ngrams from sequence, e.g. ([1,2,3], 2) -> [(1,2), (2,3)]
       Note that fewer sequence items than n results in an empty list being returned"""
    # credit: http://stackoverflow.com/questions/2380394/simple-implementation-of-n-gram-tf-idf-and-cosine-similarity-in-python
    sequence = list(sequence)
    count = max(0, len(sequence) - n + 1)
    return [tuple(sequence[i:i+n]) for i in range(count)]

def distance_bigrams_same(question_words, sentence_words):
    """Bigram distance metric, term frequency is ignored,
       0 if bigrams are identical, 1.0 if no bigrams are common"""
    terms1 = set(ngrams(question_words, 2)) # was using nltk.bigrams
    terms2 = set(ngrams(sentence_words, 2))
    shared_terms = terms1.intersection(terms2)
    all_terms = terms1.union(terms2)
    dist = 1.0
    if len(all_terms) > 0:
        dist = 1.0 - (len(shared_terms) / float(len(all_terms)))
    return dist

def calculate_cogm(question_bag, sentence_bag):

    # Lexical words in Question & Sentence
    q_lex_words = [q['tag'] for q in question_bag['question_word_tags'] if q['tag'] in lex_words]
    s_lex_words = [s['tag'] for s in sentence_bag['sentence_word_tags'] if s['tag'] in lex_words]

    # Words and tags in Question & Sentence
    question_words = [q['word'] for q in question_bag['question_word_tags']]
    question_tags = [t['tag'] for t in question_bag['question_word_tags']]

    sentence_words = [q['word'] for q in sentence_bag['sentence_word_tags']]
    sentence_tags = [t['tag'] for t in sentence_bag['sentence_word_tags']]

    bonus_value = bonus.get_bonus(question_words, question_bag['question_named_entity_types'], sentence_words,
                                  sentence_bag['sentence_named_entity_types'], sentence_tags)
    bonus_value_fraction = bonus_value
    # print bonus_value
    # A Pair for Question
    q_a_pair = calculate_a_pair(question_bag['question_named_entities'], question_bag['question_named_entity_types'], question_tags)
    q_X1 = q_a_pair['X1']
    q_Y1 = q_a_pair['Y1']

    # A Pair for Sentence
    s_a_pair = calculate_a_pair(sentence_bag['sentence_named_entities'], sentence_bag['sentence_named_entity_types'],
                                sentence_tags)
    s_X1 = s_a_pair['X1']
    s_Y1 = s_a_pair['Y1']

    # B Pair for Question
    q_X2 = bonus_value_fraction
    q_Y2 = len(set(q_lex_words))

    # B Pair for Sentence
    s_X2 = bonus_value_fraction
    s_Y2 = len(set(s_lex_words))

    # C Pair for Question
    question_relation_frequency = rc.find_relation(question_words, question_bag['question_named_entities'])
    q_X3 = question_relation_frequency['count']
    q_Y3 = question_relation_frequency['unique']

    # C Pair for Sentence
    sentence_relation_frequency = rc.find_relation(sentence_words, sentence_bag['sentence_named_entities'])
    s_X3 = sentence_relation_frequency['count']
    s_Y3 = sentence_relation_frequency['unique']
    # print s_X3, s_Y3

    # Lexical Density for Question
    q_Nlex = len(q_lex_words)
    question_lexical_density = q_Nlex / len(question_words)

    # Readability Index for Question
    question_readability_index = 0.4 * (len(question_words) + 100 * (question_bag['question_compound_words_count'] / len('question_words')))

    # ---------------------------------------------------------------------------

    # Lexical Density for Sentence
    s_Nlex = len(s_lex_words)
    sentence_lexical_density = s_Nlex / len(sentence_words)

    # Readability Index for Sentence
    sentence_readability_index = 0.4 * (len(sentence_words) + 100 * (sentence_bag['sentence_compound_words_count'] / len('sentence_words')))

    # Bigrams
    # bigram_measures = nltk.collocations.BigramAssocMeasures()
    # finder = BigramCollocationFinder.from_words(sentence_words)
    # finder.apply_freq_filter(1)
    # a = finder.ngram_fd.viewitems()
    # for i, j in a:
    #     print("{0} {1} {2}".format(i[0], i[1], j))
    matched_bigrams = distance_bigrams_same(question_words, sentence_words)
    # print matched_bigrams
    # print ",".join(sentence_words)

    # -------------------------------------------------
    # COG Calculation

    # bonus_value_fraction = (bonus_value / 2 ) / 3
    # print bonus_value_fraction

    q_cogX = ((float(q_X1) * float(question_lexical_density))  + \
             (float(q_X2) * float(question_readability_index))  + \
             (float(q_X3) * float(question_bag['punctuation_index'])) ) /  \
             (float(question_lexical_density) + float(question_readability_index) + float(question_bag['punctuation_index']))

    q_cogY = ((float(q_Y1) * float(question_lexical_density))  + \
              (float(q_Y2) * float(question_readability_index)) + \
              (float(q_Y3) * float(question_bag['punctuation_index'])) ) / \
              (float(question_lexical_density) + float(question_readability_index) + float(question_bag['punctuation_index']))
    # print "q= ", q_cogX, q_cogY

    question_cogm = {'X1': q_X1, 'X2': q_X2, 'X3': q_X3, 'Y1': q_Y1, 'Y2': q_Y2, 'Y3': q_Y3, 'cogX': q_cogX,
                     'cogY': q_cogY, 'lexical_density': question_lexical_density,
                     'readability_index': question_readability_index,
                     'punctuation_index': question_bag['punctuation_index'], 'bonus_value': bonus_value_fraction}

    s_cogX = ((float(s_X1) * float(sentence_lexical_density)) + \
              (float(s_X2) * float(sentence_readability_index)) + \
              (float(s_X3) * float(sentence_bag['punctuation_index'])) ) / \
              (float(sentence_lexical_density) + float(sentence_readability_index) + float(
                  sentence_bag['punctuation_index']))

    s_cogY = ((float(s_Y1) * float(sentence_lexical_density)) +  \
              (float(s_Y2) * float(sentence_readability_index)) + \
              (float(s_Y3) * float(sentence_bag['punctuation_index'])) ) / \
              (float(sentence_lexical_density) + float(sentence_readability_index) + float(sentence_bag['punctuation_index']))
    # print "s= ", s_cogX, s_cogY
    # print sentence_words[0], sentence_words[1], sentence_words[2], sentence_words[3], sentence_words[4], sentence_words[5]
    #
    # print "A= ", euclidean_distance(q_X1, q_Y1, s_X1, s_Y1), "Q(a)=", q_X1, q_Y1, "A(a)=", s_X1, s_Y1
    # print "B= ", euclidean_distance(q_X2, q_Y2, s_X2, s_Y2), "Q(a)=", q_X2, q_Y2, "A(a)=", s_X2, s_Y2
    # print "C= ", euclidean_distance(q_X3, q_Y3, s_X3, s_Y3), "Q(a)=", q_X3, q_Y3, "A(a)=", s_X3, s_Y3

    sentence_cogm = {'X1': s_X1, 'X2': s_X2, 'X3': s_X3, 'Y1': s_Y1, 'Y2': s_Y2, 'Y3': s_Y3, 'cogX': s_cogX,
                     'cogY': s_cogY, 'lexical_density': sentence_lexical_density,
                     'readability_index': sentence_readability_index,
                     'punctuation_index': sentence_bag['punctuation_index'], 'bonus_value': bonus_value_fraction, 'matched_bigrams': matched_bigrams}

    return {'question_cog': question_cogm , 'sentence_cog': sentence_cogm}


def find_nearest_vector(array, value):
    idx = np.array([np.linalg.norm(x+y) for (x,y) in array-value]).argmin()
    return array[idx]

def euclidean_distance(X1, Y1, X2, Y2):
    dist =  math.sqrt(math.pow((X2 - X1), 2) + math.pow((Y2 -Y1), 2))
    return dist
