# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import stemmer
from nltk.corpus import stopwords
from .models import Dictionary

def who_logic(question, comprehension):

    return question

def what_logic(question, comprehension, split_word):
    parts = question.split(split_word)
    q1 = parts[0]
    q2 = parts[1]

    named_entities = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True)]
    if q1:
        if q1 in
    return question

def what_logic(question, comprehension, split_word):
    return question

def when_logic(question, comprehension, split_word):
    return question

def where_logic(question, comprehension, split_word):
    return question

def which_logic(question, comprehension, split_word):
    return question

def why_logic(question, comprehension, split_word):
    return question

def how_logic(question, comprehension, split_word):
    return question

def how_many_logic(question, comprehension, split_word):
    return question


def find_answers(question, comprehension):

    if "ਕੌਣ" in question:
        answers = who_logic(question, comprehension, "ਕੌਣ")

    elif "ਕਿਸ" in question:
        answers = who_logic(question, comprehension, "ਕੌਣ")

    elif "ਕਿਸੇ" in question:
        answers = who_logic(question, comprehension, "ਕਿਸੇ")

    elif "ਕੀ" in question:
        answers = what_logic(question, comprehension, "ਕੀ")

    elif "ਕਦੋਂ" in question:
        answers = when_logic(question, comprehension, "ਕਦੋਂ")

    elif "ਕਿੱਥੇ" in question:
        answers = where_logic(question, comprehension, "ਕਿੱਥੇ")

    elif "ਕਿੱਥੋਂ" in question:
        answers = where_logic(question, comprehension, "ਕਿੱਥੋਂ")

    elif "ਕਿਹੜੇ" in question:
        answers = which_logic(question, comprehension, "ਕਿਹੜੇ")

    elif "ਕਿਹੜਾ" in question:
        answers = which_logic(question, comprehension, "ਕਿਹੜਾ")

    elif "ਕਿਹੜੀ" in question:
        answers = which_logic(question, comprehension, "ਕਿਹੜੀ")

    elif "ਕਿਉਂ" in question:
        answers = why_logic(question, comprehension, "ਕਿਉਂ")

    elif "ਕਿੰਨਾ" in question:
        answers = how_many_logic(question, comprehension, "ਕਿੰਨਾ")

    elif "ਕਿੰਨੀ" in question:
        answers = how_many_logic(question, comprehension, "ਕਿੰਨੀ")

    elif "ਕਿੰਨੇ" in question:
        answers = how_many_logic(question, comprehension, "ਕਿੰਨੇ")

    elif "ਕਿੰਨੀਆਂ" in question:
        answers = how_many_logic(question, comprehension, "ਕਿੰਨੀਆਂ")

    else:
        answers = None

    return answers

def filter(sentence):
    words = sentence.split(' ')
    #Stopwords removal from punjabi language file added in corpora
    filtered = [word for word in words if word not in stopwords.words('punjabi')]
    return filtered

def find_indexes(comprehension, filtered):
    patterns = [re.compile(re.escape(f)) for f in filtered if filtered]
    patterns = [re.compile(re.escape(f)) for f in filtered]

    indexes = []
    for p in patterns:
        nn = [[m.start(0), m.end(0)] for m in re.finditer(p, comprehension.ComprehensionsText)]
        indexes.append(nn)
    return indexes

version = 0.1
author = "Gursharan Singh Dhanjal"