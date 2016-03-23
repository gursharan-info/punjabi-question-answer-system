# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

def stem(word):
    if len(word) > 3:
        if word.endswith("ੀਆਂ"):
            newword = word[:len(word)-len("ਆਂ")]
        elif word.endswith("ਿਆਂ"):
            newword = word[:len(word)-len("ਆਂ")]
        elif word.endswith("ੂਆਂ"):
            newword = word[:len(word)-len("ਆਂ")]
        elif word.endswith("ੀਏ"):
            newword = word[:len(word)-len("ਏ")]
        elif word.endswith("ਈ"):
            newword = word[:len(word)-len("ਈ")]
        elif word.endswith("ੇ"):
            newword = word[:len(word)-len("ੇ")] + "ਾ"
        elif word.endswith("ੀਓ"):
            newword = word[:len(word)-len("ਓ")]
        elif word.endswith("ਵਾਂ"):
            newword = word[:len(word)-len("ਵਾਂ")]
        elif word.endswith("ਾਂ"):
            newword = word[:len(word)-len("ਾਂ")]
        elif word.endswith("ੋਂ"):
            newword = word[:len(word)-len("ੋਂ")]
        elif word.endswith("ੋ"):
            newword = word[:len(word)-len("ੋ")] + "ਾ"
        elif word.endswith("ੀਂ"):
            newword = word[:len(word)-len("ੀਂ")]
        elif word.endswith("ਵੀਂ"):
            newword = word[:len(word)-len("ਵੀਂ")]
        elif word.endswith("ਿਉਂ"):
            newword = word[:len(word)-len("ਿਉਂ")] + "ਾ"
        elif word.endswith("ੀਆ"):
            newword = word[:len(word)-len("ਆ")]
        elif word.endswith("ਿਆ"):
            newword = word[:len(word)-len("ਆ")]  + "ਾ"
        elif word.endswith("ਈਆ"):
            newword = word[:len(word)-len("ਆ")]
        else:
            newword = word
    else:
        newword = word
    return newword
