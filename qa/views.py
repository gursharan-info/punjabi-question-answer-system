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
        A = []
        B = []
        C = []
        for question in questions:
            parts = question.QuestionTagsOnly.split('\\')

            punctuations = [i+1 for i, x in enumerate(parts) if x == 'RD_PUNC']
            question.PunctuationIndex = punctuations[-1]

            ComplexWords = Dictionary.objects.filter(CompoundWord=True)
            words = question.QuestionText.split(' ')
            comp_count = len([match for match in words if match in ComplexWords])

            all_named_entities = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True)]
            current_named_entities = [m for m in words if m in all_named_entities]

            named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(dictionary__Word__in=current_named_entities).distinct()]

            X1 = len([ne for ne in words if ne in current_named_entities])
            Y1 = len(set(named_entity_types))
            A.append([X1,Y1])
            X2 = len(set(words))
            Y2 = len(set(parts))
            B.append([X2,Y2])
            X3 = X1 * Y1
            Y3 = len(set(named_entity_types))
            C.append([X3,Y3])
            question.ReadabilityIndex = 0.4 * ( (len(words) / 1) + 100 * (comp_count / len(words)))

            Nlex = parts.count('N_NN') + parts.count('N_NNP') + parts.count('V_VM') + parts.count('V_VM_VNF') + parts.count('V_VM_VINF') + parts.count('V_VM_VNG') + parts.count('V_VAUX') + parts.count('JJ') + parts.count('RB')
            question.LexicalDensity = "%.2f" % round( Nlex / len(parts), 2)

            question.cogX = ((float(X1) * float(question.LexicalDensity)) + (float(X2) * float(question.ReadabilityIndex)) + (float(X3) * float(question.PunctuationIndex) ) ) / (float(question.LexicalDensity) + float(question.ReadabilityIndex) + float(question.PunctuationIndex))
            question.cogY = ((float(Y1) * float(question.LexicalDensity)) + (float(Y2) * float(question.ReadabilityIndex)) + (float(Y3) * float(question.PunctuationIndex) ) ) / (float(question.LexicalDensity) + float(question.ReadabilityIndex) + float(question.PunctuationIndex))
            question.center_of_gravity = ujson.dumps([question.cogX,question.cogY])

    except Comprehension.DoesNotExist:
        raise Http404('Comprehension does not exist')
    return render(request,  'qa/compdetail.html', {'comprehension': comprehension, 'questions': questions, 'complexwords':
        ComplexWords, 'words': current_named_entities, 'A': A,'B': B, 'C':C})

def questiondetail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question_types = question.QuestionTypeID.all()
        comprehension = Comprehension.objects.get(pk=question.Comprehension_id)
        parts = question.QuestionTagsOnly.split('\\')

        punctuations = [i+1 for i, x in enumerate(parts) if x == 'RD_PUNC']
        question.PunctuationIndex = punctuations[-1]

        ComplexWords = Dictionary.objects.filter(CompoundWord=True)
        words = question.QuestionText.split(' ')
        comp_count = len([match for match in words if match in ComplexWords])

        all_named_entities = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True)]
        current_named_entities = [m for m in words if m in all_named_entities]

        named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(dictionary__Word__in=current_named_entities).distinct()]

        X1 = len([ne for ne in words if ne in current_named_entities])
        Y1 = len(set(named_entity_types))
        X2 = len(set(words))
        Y2 = len(set(parts))
        X3 = X1 * Y1
        Y3 = len(set(named_entity_types))
        question.ReadabilityIndex = 0.4 * ( (len(words) / 1) + 100 * (comp_count / len(words)))

        Nlex = parts.count('N_NN') + parts.count('N_NNP') + parts.count('V_VM') + parts.count('V_VM_VNF') + parts.count('V_VM_VINF') + parts.count('V_VM_VNG') + parts.count('V_VAUX') + parts.count('JJ') + parts.count('RB')
        question.LexicalDensity = "%.2f" % round( Nlex / len(parts), 2)

        question.cogX = ((float(X1) * float(question.LexicalDensity)) + (float(X2) * float(question.ReadabilityIndex)) + (float(X3) * float(question.PunctuationIndex) ) ) / (float(question.LexicalDensity) + float(question.ReadabilityIndex) + float(question.PunctuationIndex))
        question.cogY = ((float(Y1) * float(question.LexicalDensity)) + (float(Y2) * float(question.ReadabilityIndex)) + (float(Y3) * float(question.PunctuationIndex) ) ) / (float(question.LexicalDensity) + float(question.ReadabilityIndex) + float(question.PunctuationIndex))
        question.center_of_gravity = ujson.dumps([question.cogX,question.cogY])

        questiondata = [
            ['X','Y'],
            [X1,Y1],
            [X2,Y3],
            [X3,Y3]
        ]

        xdata = [X1,X2,X3]
        ydata = [Y1,Y2,Y3]
        cogdata = [question.cogX, question.cogY]

        dataset = [
            {
                'label': 'Points',
                'data': xdata,
                'points': {'symbol': "circle", 'fillColor': "#FF0000", 'show': 'true'},
                'lines': {'show': 'true'},
            },
            {
                'label': 'COG',
                'data': ydata,
                'points': {'symbol': "triangle", 'fillColor': "#FF0000", 'show': 'true'},
            }
        ]

        graph = flot.PointChart(SimpleDataSource(data=questiondata))

        testtext = question.QuestionText
        from nltk.corpus import stopwords

        #nltk.word_tokenize vs split
        testwords = testtext.split(' ')

        def find_all(str, substr):
            start = 0
            while True:
                start = str.find(substr,start)
                if start == -1:return
                yield start
                start += len(substr)  # use len(substr) for non overlapping matches


        filtered = [word for word in words if word not in stopwords.words('punjabi')]
    #    patterns = [re.compile(re.escape(f)) for f in filtered if filtered]
    #    ##text = [(f.start(), f.end()) for f in list(re.finditer(ww, comprehension.ComprehensionsText))]
    #    patt = re.compile(ww)
    #   text = [m.start() for m in re.finditer(ww, comprehension.ComprehensionsText)]
    #   text = re.match(patt, comprehension.ComprehensionsText)
        patterns = [re.compile(re.escape(f)) for f in filtered]

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
    return render(request,  'qa/questiondetail.html', {'comprehension': comprehension, 'question': question, 'X':[X1,X2,X3], 'Y':[Y1,Y2,Y3], 'graph': graph, 'filtered': filtered, 'question_types': question_types})