# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import stemmer
import ngram
thismodule = sys.modules[__name__]

def check_question_type(question):
    type = None
    question_words = question.split()
    if "ਕਿਵੇਂ" in question_words:
        type = {'function': 'how', 'q_word': "ਕਿਵੇਂ"}
    elif "ਕੀ-ਕੀ" in question_words:
        type = {'function': 'what', 'q_word': "ਕੀ-ਕੀ"}
    elif "ਕੀ" in question_words:
        type = {'function': 'what', 'q_word': "ਕੀ"}
    elif "ਕਦੋਂ" in question_words:
        type = {'function': 'when', 'q_word': "ਕਦੋਂ"}
    elif "ਕਿੱਥੇ" in question_words:
        type = {'function': 'where', 'q_word': "ਕਿੱਥੇ"}
    elif "ਕਿੱਥੋਂ" in question_words:
        type = {'function':'where', 'q_word': "ਕਿੱਥੋਂ"}
    elif "ਕਿਹੜਾ" in question_words:
        type = {'function': 'which', 'q_word': "ਕਿਹੜਾ"}
    elif "ਕਿਹੜੀ" in question_words:
        type = {'function': 'which', 'q_word': "ਕਿਹੜੀ"}
    elif "ਕਿਹੜੀਆਂ" in question_words:
        type = {'function': 'which', 'q_word': "ਕਿਹੜੀਆਂ"}
    elif "ਕਿਹੜੇ-ਕਿਹੜੇ" in question_words:
        type = {'function': 'which', 'q_word': "ਕਿਹੜੇ-ਕਿਹੜੇ"}
    elif "ਕਿਹੜੇ" in question_words:
        type = {'function': 'which', 'q_word': "ਕਿਹੜੇ"}
    elif "ਕੌਣ-ਕੌਣ" in question_words:
        type = {'function': 'who', 'q_word': "ਕੌਣ-ਕੌਣ"}
    elif "ਕੌਣ" in question_words:
        type = {'function': 'who', 'q_word': "ਕੌਣ"}
    # elif any(("ਕਿਸ ਤਰ੍ਹਾਂ","ਕਿਸ ਤਰਾਂ")) in question_words:
    #     type = {'function': 'how', 'q_word': "ਕਿਸ"}
    elif "ਕਿਸ-ਕਿਸ" in question_words:
        type = {'function': 'who', 'q_word': "ਕਿਸ-ਕਿਸ"}
    elif "ਕਿਸ" in question_words:
        type = {'function': 'who', 'q_word': "ਕਿਸ"}
    elif "ਕਿਸੇ" in question_words:
        type = {'function': 'who', 'q_word': "ਕਿਸੇ"}
    elif "ਕਿਉਂ" in question_words:
        type = {'function': 'why', 'q_word': "ਕਿਉਂ"}
    elif "ਕਿਹੋ-ਜਿਹੀ" in question_words:
        type = {'function': 'what_kind_type', 'q_word': "ਕਿਹੋ-ਜਿਹੀ"}
    elif "ਕਿਹੋ-ਜਿਹੇ" in question_words:
        type = {'function': 'what_kind_type', 'q_word': "ਕਿਹੋ-ਜਿਹੇ"}
    elif "ਕਿਹੋ-ਜਿਹਾ" in question_words:
        type = {'function': 'what_kind_type', 'q_word': "ਕਿਹੋ-ਜਿਹਾ"}
    elif "ਕਿਹੋ-ਜਿਹੀਆਂ" in question_words:
        type = {'function': 'what_kind_type', 'q_word': "ਕਿਹੋ-ਜਿਹੀਆਂ"}
    elif "ਕਿੰਨਾ" in question_words:
        type = {'function': 'how_much', 'q_word': "ਕਿੰਨਾ"}
    elif "ਕਿੰਨੀ" in question_words:
        type = {'function': 'how_much', 'q_word': "ਕਿੰਨੀ"}
    elif "ਕਿੰਨੀ-ਕਿੰਨੀ" in question_words:
        type = {'function': 'how_much', 'q_word': "ਕਿੰਨੀ-ਕਿੰਨੀ"}
    elif "ਕਿੰਨੇ" in question_words:
        type = {'function': 'how_many', 'q_word': "ਕਿੰਨੇ"}
    elif "ਕਿੰਨੀਆਂ" in question_words:
        type = {'function': 'how_many', 'q_word': "ਕਿੰਨੀਆਂ"}
    return type

def split_question(question, question_word):
    parts = question.split(question_word)
    print question_word
    q1 = parts[0].strip()
    q2 = parts[1].strip()
    return {'q1': parts[0].split(), 'q2': parts[1].split()}

def get_named_entities(types):
    from qa.models import Dictionary
    all_named_entities = []
    for t in types:
        types_extracted = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True, NamedEntityTypeID__name__exact=t)]
        for tt in types_extracted:
            all_named_entities.append(tt)
    return all_named_entities

def check_named_entities(text):
    text_words = text.split(" ")
    all_named_entities = get_named_entities()
    text_named_entities = [m for m in text_words if m in all_named_entities]
    return text_named_entities

def extract_answer_from_array(start, end, array):

    start = 0 if start < 0 else start
    end = len(array)-1 if end > len(array)-1 else end

    list = array[start:end]
    string = " ".join(list)

    return string

def who_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    named_entities = get_named_entities(['person', 'organization'])
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities):
            probable_answers.append(sentence + " |")
    return probable_answers

def what_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    named_entities = get_named_entities(['person', 'object'])
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                " ਕਿ " in sentence or \
                any(word in sentence_words for word in named_entities):
            probable_answers.append(sentence + " |")
    return probable_answers

def what_kind_type_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    match_words = ['ਇਹੋ','ਜਿਹਾ','ਜਿਹੇ','ਤਰ੍ਹਾਂ','ਤਰਾਂ']
    named_entities = get_named_entities(['object'])
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities):
            probable_answers.append(sentence + " |")
    return probable_answers

def when_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    match_words =['ਸਮੇਂ','ਵੇਲੇ','ਵੇਲ੍ਹੇ']
    named_entities = get_named_entities(['time', 'date'])
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities) or \
                any(word in sentence_words for word in match_words):
            probable_answers.append(sentence + " |")
    return probable_answers

def which_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    named_entities = get_named_entities(['object', 'organisation', 'date'])
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words    = sentence.split()
        # print " ".join([s for s in sentence])
        # sentence_stemmed = [stemmer.stem(word) for word in sentence]
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities):
            probable_answers.append(sentence + " |")
    # probable_answers = [word.strip() + " |" for word in comprehension.split("|")]
    # del probable_answers[-1]
    return probable_answers

def where_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    match_words = ['ਜਿੱਥੇ','ਜਿਥੇ','ਉਥੇ','ਉੱਥੇ','ਓਥੇ','ਜਗਾ','ਜਗ੍ਹਾ','ਜਿੱਥੋਂ','ਜਿਥੋਂ','ਉਥੋਂ','ਓਥੋਂ']
    named_entities = get_named_entities(['location'])
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities) or \
                any(word in sentence_words for word in match_words):
            probable_answers.append(sentence + " |")
    return probable_answers

def why_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    match_words = ['ਕਿਉਂ','ਇਸ ਲਈ']
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in match_words):
            probable_answers.append(sentence + " |")
    return probable_answers


def how_many_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    named_entities = get_named_entities(['numbers','money', 'quantity'])
    match_words = ['ਐਨੇ', 'ਏਨੇ', 'ਇੰਨੇ', 'ਜਿੰਨੇ', 'ਕਿੰਨੀਆਂ', 'ਓਨੀਆਂ', 'ਉਨੀਆਂ', 'ਏਨੀਆਂ', 'ਐਨੀਆਂ']
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities) or \
                any(word in sentence_words for word in match_words):
            probable_answers.append(sentence + " |")
    return probable_answers


def how_much_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    named_entities = get_named_entities(['numbers', 'money', 'quantity'])
    match_words = ['ਕਿੰਨਾ', 'ਉਨਾ', 'ਓਨਾ', 'ਐਨਾ', 'ਏਨਾ', 'ਜਿੰਨੀ', 'ਓਨੀ', 'ਉਨੀ', 'ਏਨੀ', 'ਐਨੀ']
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in named_entities) or \
                any(word in sentence_words for word in match_words):
            probable_answers.append(sentence + " |")
    return probable_answers

def how_logic(question, question_word, comprehension):
    question_parts = split_question(question, question_word)
    match_words = ['ਇਸ ਤਰ੍ਹਾਂ','ਇਸ ਤਰਾਂ','ਜਿਵੇਂ','ਉਵੇਂ','ਓਵੇਂ','ਓਦਾਂ','ਐਵੇਂ','ਏਦਾਂ']
    probable_answers = []
    sentences = [word.strip() for word in comprehension.split("|")]

    for sentence in sentences:
        sentence_words = sentence.split()
        bigrams_dissimilarity = ngram.bigrams_dissimilarity(question.split(), sentence_words)
        if any(word in sentence_words for word in question_parts['q1']) or \
                any(word in sentence_words for word in question_parts['q2']) or \
                any(word in sentence_words for word in match_words):
                # bigrams_dissimilarity < 0.5:
            probable_answers.append(sentence + " |")
    return probable_answers


def formulate(question, comprehension):
    import re
    comprehension = re.sub(r'([\'\"])', '', comprehension)
    question_type = check_question_type(question)
    if question_type:
        question_type_function_name = question_type['function'] + "_logic"
        question_type_function_call = getattr(thismodule, question_type_function_name)
        sentences = question_type_function_call(question, question_type['q_word'], comprehension)
        output = {'sentences':sentences, 'empty': False}
    else:
        output = {'sentences':[], 'empty': True}
    return output

# def create_answers(comprehension, answer_hint):

