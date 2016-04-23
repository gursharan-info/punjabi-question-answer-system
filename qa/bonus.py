# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

def get_bonus(question_words, sentence_words):

    matches = len([match for match in sentence_words if match in question_words])
    #print matches
    if matches < 1:
        bonus = 1 / len(sentence_words)
    else:
        bonus = matches / len(sentence_words)

    return bonus