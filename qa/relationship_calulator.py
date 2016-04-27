# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

relationships = [
    "ਨੇ",
    "ਨੂੰ",
    "ਤੋਂ",
    "ਨਾਲ",
    "ਦੁਆਰਾ",
    "ਲਈ",
    "ਦਾ",
    "ਦੇ",
    "ਦੀ",
    "ਵਿਚ",
    "ਵਿੱਚ",
    "ਤੇ",
    "ਨੀਚੇ",
    "ਉੱਪਰ",
    "ਨੀਵਾਂ",
    "ਉੱਤੇ",
    "ਨੇੜੇ",
    "ਨੇੜ੍ਹੇ",
    "ਦੂਰ",
    "ਅੱਗੇ",
    "ਪਿੱਛੇ",
    "ਅੰਦਰ",
    "ਬਾਹਰ",
    "ਪਹਿਲਾਂ",
    "ਬਾਅਦ"
]
def find_relation(words, named_entities):

    relation_list = []
    if len(named_entities) >= 2:
        for relation in relationships:
            if relation in words:
                relation_list.append(relation)

    relation_frequencies = len(relation_list)

    if relation_frequencies < 1:
        relationship_count = {'count': 1, 'unique': 1}
    else:
        relationship_count = {'count': relation_frequencies, 'unique': len(set(relation_list))}

    return relationship_count

