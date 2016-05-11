# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division


def get_bonus(question_words, question_named_entity_types, sentence_words, sentence_named_entity_types, sentence_tags):

    unique_question_words = question_words
    unique_sentence_words = sentence_words

    bonus_x = len(set([match for match in unique_sentence_words if match in unique_question_words]))

    # Bonus_X
    # Bonus_Y

    bonus_y = 0

    if "ਕੌਣ" in question_words:
        nes = len([n for n in ["person", "organization"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes

    elif "ਕਿਨ੍ਹਾਂ" or "ਕਿੰਨ੍ਹਾਂ" or "ਕਿਨ੍ਹਾ" in question_words:
        nes = len([n for n in ["person", "organization"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes

    elif "ਕਿਸ" or "ਕਿਸੇ" in question_words:
        nes = len([n for n in ["person", "organization"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes

    elif "ਕੀ" in question_words:
        nes = len([n for n in ["person", "object"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes

        verbs = ['V__VM', 'V__VM__VNF', 'V__VAUX']
        verb_matches = len([n for n in verbs if n in sentence_tags])
        if verb_matches >= 1:
            bonus_y += verb_matches

    elif "ਕਦੋਂ" in question_words:
        nes = len([n for n in ["time", "date"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes

        match_strings = ["ਪਹਿਲਾਂ","ਬਾਅਦ","ਜਦੋਂ","ਉਦੋਂ","ਓਦੋਂ","ਜਦ","ਸਮੇਂ","ਵੇਲੇ","ਵੇਲ੍ਹੇ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

    elif "ਕਿੱਥੇ" in question_words:
        if "location" in sentence_named_entity_types:
            bonus_y += 1
        location_words = ['ਜਿਥੇ', 'ਜਿੱਥੇ', 'ਉਥੇ', 'ਉੱਥੇ', 'ਜਗਾ', 'ਜਗ੍ਹਾ']
        location_matches = len([l for l in location_words if l in sentence_words])
        if location_matches >= 1:
            bonus_y += location_matches

    elif "ਕਿੱਥੋਂ" in question_words:
        if "location" in sentence_named_entity_types:
            bonus_y += 1
        location_words = ['ਜਿਥੇ', 'ਜਿੱਥੇ', 'ਉਥੇ', 'ਉੱਥੇ', 'ਜਗਾ', 'ਜਗ੍ਹਾ']
        location_matches = len([l for l in location_words if l in sentence_words])
        if location_matches >= 1:
            bonus_y += location_matches

    elif "ਕਿਹੜੇ" in question_words:
        nes = len([n for n in ["organization", "object", "date"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        verbs = ['V__VM', 'V__VM__VNF', 'V__VAUX']
        verb_matches = len([n for n in verbs if n in sentence_tags])
        if verb_matches >= 1:
            bonus_y += verb_matches

    elif "ਕਿਹੜਾ" in question_words:
        nes = len([n for n in ["organization", "object", "date"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        verbs = ['V__VM', 'V__VM__VNF', 'V__VAUX']
        verb_matches = len([n for n in verbs if n in sentence_tags])
        if verb_matches >= 1:
            bonus_y += verb_matches

    elif "ਕਿਹੜੀ" in question_words:
        nes = len([n for n in ["organization", "object", "date"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        verbs = ['V__VM', 'V__VM__VNF', 'V__VAUX']
        verb_matches = len([n for n in verbs if n in sentence_tags])
        if verb_matches >= 1:
            bonus_y += verb_matches

    elif "ਕਿਉਂ" in question_words:
        match_strings = ["ਕਿਉਂ", "ਇਸ ਲਈ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

    elif "ਕਿੰਨਾ" in question_words:
        nes = len([n for n in ["numbers", "money", "quantity"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        match_strings = ["ਜਿੰਨਾ", "ਉਨਾ", "ਓਨਾ", "ਐਨਾ", "ਏਨਾ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

    elif "ਕਿੰਨੀ" in question_words:
        nes = len([n for n in ["numbers", "money", "quantity"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        match_strings = ["ਜਿੰਨੀ", "ਓਨੀ", "ਉਨੀ", "ਏਨੀ", "ਐਨੀ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

    elif "ਕਿੰਨੇ" in question_words:
        nes = len([n for n in ["numbers", "money", "quantity"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        match_strings = ["ਐਨੇ", "ਏਨੇ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

    elif "ਕਿੰਨੀਆਂ" in question_words:
        nes = len([n for n in ["numbers", "money", "quantity"] if n in sentence_named_entity_types])
        if nes >= 1:
            bonus_y += nes
        match_strings = ["ਜਿੰਨੀਆਂ", "ਓਨੀਆਂ", "ਉਨੀਆਂ", "ਏਨੀਆਂ", "ਐਨੀਆਂ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

    elif "ਕਿਵੇਂ" in question_words:
        match_strings = ["ਕਰਕੇ", "ਜਿਵੇਂ", "ਉਵੇਂ", "ਓਵੇਂ", "ਓਦਾਂ", "ਐਵੇਂ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches

        verbs = ['V__VM', 'V__VM__VNF', 'V__VAUX']
        verb_matches = len([n for n in verbs if n in sentence_tags])
        if verb_matches >= 1:
            bonus_y += verb_matches

    elif "ਕਿਹੋ ਜਿਹਾ" or "ਕਿਹੋ ਜਿਹੇ" in question_words:
        match_strings = ["ਇਹੋ ਜਿਹਾ", "ਇਹੋ ਜਿਹੇ"]
        word_matches = len([m for m in match_strings if m in sentence_words])
        if word_matches >= 1:
            bonus_y += word_matches


    return {'bonus_x':bonus_x, 'bonus_y': bonus_y}
