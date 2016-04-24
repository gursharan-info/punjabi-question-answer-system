# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.http import Http404
from django.shortcuts import render
from datetime import datetime
import ujson
from django.http import HttpResponse
from django.template import loader
from .models import Comprehension, Question, Dictionary, NamedEntityType, Answer, QuestionType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from graphos.sources.simple import SimpleDataSource
from graphos.renderers import flot
import re
import string
from django.db.models import Count
from scipy import spatial
import numpy as np
import cogm
import bonus
import random
from operator import itemgetter
# Create your views here.


def index(request):
    return render(request,  'qa/index.html', {})

def comprehensions(request):
    comprehension_list = Comprehension.objects.order_by('-LastUpdate')
    paginator = Paginator(comprehension_list, 20) # Show 20 items per page

    page = request.GET.get('page')
    try:
        comprehensions = paginator.page(page)
    except PageNotAnInteger:
         #If page is not an integer, deliver first page.
        comprehensions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comprehensions = paginator.page(paginator.num_pages)
    return render(request,  'qa/comprehensions.html', {'comprehensions': comprehensions, 'callout_list':['success','warning','danger','info']})

def dictionary(request):
    dictionary_list = Dictionary.objects.all().order_by('-LastUpdate')
    paginator = Paginator(dictionary_list, 50) # Show 50 items per page

    page = request.GET.get('page')
    try:
        dictionarywords = paginator.page(page)
    except PageNotAnInteger:
         #If page is not an integer, deliver first page.
        dictionarywords = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        dictionarywords = paginator.page(paginator.num_pages)

    return render(request,  'qa/dictionary.html', {'dictionarywords': dictionarywords})

def patterns(request):
    from collections import Counter

    question_patterns = Question.objects.all()
    sequences = [q.QuestionTagsOnly for q in question_patterns]
    patterns = Counter(sequences).most_common()

    return render(request,  'qa/patterns.html', {'patterns': patterns})

def top_patterns(request):
    from collections import Counter

    question_patterns = Question.objects.all()
    sequences = [q.QuestionTagsOnly for q in question_patterns]
    patterns = Counter(sequences).most_common(10)

    #questions = [Question.objects.filter(QuestionTagsOnly=pattern[0]) for pattern in patterns]

    return render(request,  'qa/toppatterns.html', {'questions': patterns})

def compdetail(request, comprehension_id):
    try:
        comprehension = Comprehension.objects.get(pk=comprehension_id)
        questions = Question.objects.select_related().filter(Comprehension=comprehension_id)


    except Comprehension.DoesNotExist:
        raise Http404('Comprehension does not exist')
    return render(request,  'qa/compdetail.html', {'comprehension': comprehension, 'questions': questions})

def questions(request):

    question_types = QuestionType.objects.all()

    questions = []
    for type in question_types:
        type_list = [Question.objects.filter(QuestionTypeID=type), type]
        questions.append(type_list)

    #types = QuestionType.objects.annotate(count=Count('questiontypes')).order_by('-count').values('id', 'count')
    return render(request,  'qa/questions.html', {'questions': questions,})

def questiondetail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question_types = question.QuestionTypeID.all()
        comprehension = Comprehension.objects.get(pk=question.Comprehension_id)

        # Split Question tags string into individual tags
        tag_parts = question.QuestionTagsOnly.split('\\')

        # Find Punctuation Index (W3)
        punctuations = [i+1 for i, x in enumerate(tag_parts) if x == 'RD_PUNC']
        punctuation_index = punctuations[-1]

        #Fetch compound words from the dictionary and count their matches against question words
        compound_words = Dictionary.objects.filter(CompoundWord=True)
        question_words = question.QuestionText.split(' ')
        compound_words_count = len([match for match in question_words if match in compound_words])

        all_named_entities = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True)]
        current_named_entities = [m for m in question_words if m in all_named_entities]

        question_named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(dictionary__Word__in=current_named_entities).distinct()]

        question_cog = cogm.calculate_cogm(question_words, punctuation_index, compound_words_count, question_named_entity_types, tag_parts, current_named_entities)
        question.center_of_gravity = question_cog
        question_cog['question'] = question.QuestionText
        question_cog['question_tagged'] = tag_parts
        #print "q= ", question_cog


        # Break paragraph into sentences
        sentences = [s.strip() + " |" for s in comprehension.ComprehensionsText.split('|')]
        del sentences[-1]

        probable_answers = []
        tags = []
        answers_cog_list = []
        for sentence_index, sentence in enumerate(sentences):

            sentence_words = sentence.split()

            sentence_compound_words_count = len([match for match in sentence_words if match in compound_words])

            sentence_named_entities = [m for m in sentence_words if m in all_named_entities]
            sentence_named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(dictionary__Word__in=sentence_named_entities).distinct()]

            # print sentence_named_entity_types

            # Split Question tags string into individual tags
            tag_parts = [Dictionary.objects.filter(Word=w).values_list('WordType', flat=True) for w in sentence_words]

            sentence_tags = []
            for part in tag_parts:
                for p in part:
                    sentence_tags.append(p)

            #sentence_tags.append('RD_PUNC')

            # temporay variable to print tags on webpage
            tags.append(sentence_tags)

            #Find Punctuation Index (W3)
            punctuations = [iter + 1 for iter, punc in enumerate(sentence_tags) if punc == 'RD_PUNC']

            punctuation_index = punctuations[-1]
            #print sentence_compound_words_count
            sentence_cog = cogm.calculate_cogm(sentence_words, punctuation_index, sentence_compound_words_count, sentence_named_entity_types, sentence_tags, sentence_named_entities)

            # returned 0-sentence, 1-cogx, 2-cogy, 3-cog pair, 4-sentence_index, 5-lexical_density 6-readability_index, 7-punctuation_index
            #bonus_value = bonus.get_bonus(question_words, sentence_words)

            # answer.AnswerText = sentence
            # answer.cogX = sentence_cog[0]
            # answer.cogY = sentence_cog[1]
            #
            # answer.center_of_gravity = [sentence_cog[0],sentence_cog[1]]
            #
            # answer.SentenceIndex = sentence_index+1
            # answer.LexicalDensity = sentence_cog[2]
            # answer.ReadabilityIndex = sentence_cog[3]
            # answer.PunctuationIndex = punctuation_index
            euclidean_distance = cogm.euclidean_distance(sentence_cog['cogX'], sentence_cog['cogY'], question_cog['cogX'], question_cog['cogY'])
            # print sentence_cog['cogX'], sentence_cog['cogY']
            print euclidean_distance
            bonus_value = bonus.get_bonus(question_words, question_named_entity_types, sentence_words, sentence_named_entity_types, sentence_tags)
            print bonus_value
            # bonus_value = 1
            probable_answer = {'sentence': sentence, 'sentence_tags': sentence_tags,'cogX': sentence_cog['cogX'], 'cogY': sentence_cog['cogY'], 'cog': [sentence_cog['cogX'], sentence_cog['cogY']],
                               'sentence_index': sentence_index + 1, 'lexical_density': sentence_cog['lexical_density'],
                               'readability_index': sentence_cog['readability_index'], 'punctuation_index': punctuation_index, 'euclidean_distance': euclidean_distance, 'bonus': bonus_value, 'sentence_cog': sentence_cog }
            #print probable_answer
            answers_cog_list.append([sentence_cog['cogX'],sentence_cog['cogY']])
            #print sentence
            probable_answers.append(probable_answer)
        # answers = sorted(probable_answers, key=itemgetter('euclidean_distance'), reverse=True)
        answers = probable_answers
        answers_cog = np.array(answers_cog_list)
        #print answers_cog
        #random.shuffle(answers)

        nearest_answer = cogm.find_nearest_vector(answers_cog, [question_cog['cogX'], question_cog['cogY']])
        #print nearest_answer

        # questiondata = [
        #     ['X','Y'],
        #     [question_cog['X1'],question_cog['Y1']],
        #     [question_cog['X2'],question_cog['Y3']],
        #     [question_cog['X3'],question_cog['Y3']],
        # ]
        # print questiondata
        #
        # xdata = [X1,X2,X3]
        # ydata = [Y1,Y2,Y3]
        # cogdata = [question.cogX, question.cogY]
        #
        # options = [
        #     {
        #         'label': 'Points',
        #         'data': questiondata,
        #         'points': {'symbol': "circle", 'fillColor': "#FF0000", 'show': 'true'},
        #         'lines': {'show': 'false'},
        #     },
        #     {
        #         'label': 'Points',
        #         'data': [question_cog['cogX'], question_cog['cogY']],
        #         'points': {'symbol': "circle", 'fillColor': "#FF0000", 'show': 'true'},
        #         'lines': {'show': 'false'},
        #     }
        # ]

        # graph = flot.PointChart(SimpleDataSource(data=questiondata))
        #
        # testtext = question.QuestionText
        # from nltk.corpus import stopwords
        #
        # #nltk.word_tokenize vs split
        # testwords = testtext.split(' ')
        #
        # def find_all(str, substr):
        #     start = 0
        #     while True:
        #         start = str.find(substr,start)
        #         if start == -1:return
        #         yield start
        #         start += len(substr)  # use len(substr) for non overlapping matches


    #    filtered = [word for word in words if word not in stopwords.words('punjabi')]
    #    patterns = [re.compile(re.escape(f)) for f in filtered if filtered]
    #    ##text = [(f.start(), f.end()) for f in list(re.finditer(ww, comprehension.ComprehensionsText))]
    #    patt = re.compile(ww)
    #   text = [m.start() for m in re.finditer(ww, comprehension.ComprehensionsText)]
    #   text = re.match(patt, comprehension.ComprehensionsText)
    #    patterns = [re.compile(re.escape(f)) for f in filtered]

        # hints = []
        # lengths = []
        # for p in patterns:
        #     nn = [comprehension.ComprehensionsText[m.start(0)-30:m.end(0)+30] for m in re.finditer(p, comprehension.ComprehensionsText)]
        #     first_split = [sent.split(' ', 1)[1] for sent in nn if len(sent.split(' ', 1)[1]) > 3]
        #     second_split = [sent.rsplit(' ', 1)[0] for sent in first_split if len(sent.split(' ', 1)[0]) > 3]
        #     hints.append(second_split)
        #     lengths.append([len(sent.rsplit(' ', 1)[1]) for sent in nn if sent])
            #hints.append(nn)
        # index = hints[0]
        # findex = index[0]
        # pairs = []
        # answers = []
        # for questiontype in question_types:
        #     pair = string.split(question.QuestionText, questiontype.QuestionType)
        #     pairs.append(pair)
        #
        #     answers.append(qas.find_answers(question.QuestionText, questiontype.QuestionType, pair[0], pair[1]))


    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    #return render(request,  'qa/questiondetail.html', {'comprehension': comprehension, 'question': question, 'X':[X1,X2,X3], 'Y':[Y1,Y2,Y3], 'graph': graph, 'question_types': question_types})
    return render(request, 'qa/questiondetail.html',
                  {'comprehension': comprehension, 'question': question, 'q_cog_dump': ujson.dumps(question_cog), 'question_types': question_types, 'answers': answers, 'answers_dump': ujson.dumps(answers), 'tags': tags})