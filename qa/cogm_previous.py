# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import numpy as np
import math
import relationship_calulator as rc
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

def calculate_cogm(words, punctuation_index, compound_words_count, named_entity_types, tag_parts, current_named_entities):

    X1 = len([ne for ne in words if ne in current_named_entities])
    Y1 = len(set(named_entity_types))

    sentence_lex_words = []

    for w,t in zip(words, tag_parts):
        print w,t

    Nlex = tag_parts.count('N_NN') + tag_parts.count('N_NNP') + tag_parts.count('V_VM') + tag_parts.count(
        'V_VM_VNF') + tag_parts.count('V_VM_VINF') + tag_parts.count('V_VM_VNG') + tag_parts.count(
        'V_VAUX') + tag_parts.count('JJ') + tag_parts.count('RB')

    X2 = len(set(words))
    Y2 = len(set(tag_parts))

    relation_frequency = rc.find_relation(words, current_named_entities)
    # print relation_frequency
    X3 = relation_frequency['count']
    Y3 = relation_frequency['unique']

    readability_index = 0.4 * (len(words) + 100 * (compound_words_count / len(words)))
    lexical_density = Nlex / len(set(words))

    cogX = ((float(X1) * float(lexical_density)) + (float(X2) * float(readability_index)) + (float(X3) * float(punctuation_index))) / (float(lexical_density) + float(readability_index) + float(punctuation_index))
    cogY = ((float(Y1) * float(lexical_density)) + (float(Y2) * float(readability_index)) + (float(Y3) * float(punctuation_index))) / (float(lexical_density) + float(readability_index) + float(punctuation_index))
    #print [cogX, cogY]

    cogm = {'X1': X1, 'X2': X2,'X3': X3,'Y1': Y1,'Y2': Y2,'Y3': Y3,'cogX': cogX, 'cogY':cogY, 'lexical_density': lexical_density, 'readability_index': readability_index, 'punctuation_index': punctuation_index}
    return cogm


def find_nearest_vector(array, value):
    idx = np.array([np.linalg.norm(x+y) for (x,y) in array-value]).argmin()
    return array[idx]

def euclidean_distance(X1, Y1, X2, Y2):
    dist =  math.sqrt(math.pow((X2 - X1), 2) + math.pow((Y2 -Y1), 2))
    return dist
