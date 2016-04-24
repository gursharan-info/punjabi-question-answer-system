# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

def get_bonus(question_words, question_named_entity_types, sentence_words, sentence_named_entity_types, sentence_tags):

    matches = len([match for match in sentence_words if match in question_words])
    #print matches
    # print sentence_tags
    if matches < 1:
        bonus = 1
    else:
        bonus = matches

    if "ਕੌਣ" in question_words:
        if ("person" in sentence_named_entity_types) or ("organization" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿਸ" in question_words:
        if ("person" in sentence_named_entity_types) or ("organization" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿਸੇ" in question_words:
        if ("person" in sentence_named_entity_types) or ("organization" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕੀ" in question_words:
        if ("object" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਦੋਂ" in question_words:
        if ("time" in sentence_named_entity_types) or ("date" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿੱਥੇ" in question_words:
        if ("location" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿੱਥੋਂ" in question_words:
        if ("location" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿਹੜੇ" in question_words:
        bonus += 1
    elif "ਕਿਹੜਾ" in question_words:
        bonus += 1
    elif "ਕਿਹੜੀ" in question_words:
        bonus += 1
    elif "ਕਿਉਂ" in question_words:
        bonus += 1
    elif "ਕਿੰਨਾ" in question_words:
        if ("quantity" in sentence_named_entity_types) or ("numbers" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿੰਨੀ" in question_words:
        if ("quantity" in sentence_named_entity_types) or ("numbers" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿੰਨੇ" in question_words:
        if ("quantity" in sentence_named_entity_types) or ("numbers" in sentence_named_entity_types):
            print 'yes'
        bonus += 1
    elif "ਕਿੰਨੀਆਂ" in question_words:
        if ("quantity" in sentence_named_entity_types) or ("numbers" in sentence_named_entity_types):
            print 'yes'
        bonus += 1


    return bonus