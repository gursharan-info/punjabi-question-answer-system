# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import stemmer
from nltk.corpus import stopwords

def find_answers(question, questiontype, X1, Y1):


    if questiontype == "ਕੌਣ":

    elif questiontype == "ਕਿਸ":


    elif questiontype == "ਕਿਸੇ":
            

    elif questiontype == "ਕੀ":
            

    elif questiontype == "ਕਦੋਂ":
            

    elif questiontype == "ਕਿੱਥੇ":
            

    elif questiontype == "ਕਿੱਥੋਂ":
            

    elif questiontype == "ਕਿਹੜੇ":
            

    elif questiontype == "ਕਿਹੜਾ":
            

    elif questiontype == "ਕਿਹੜੀ":
            

    elif questiontype == "ਕਿਉਂ":
            

    elif questiontype == "ਕਿੰਨਾ":
            

    elif questiontype == "ਕਿੰਨੀ":
            

    elif questiontype == "ਕਿੰਨੇ":
            

    elif questiontype == "ਕਿੰਨੀਆਂ":
            

    else:
            


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
