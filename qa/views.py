# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.http import Http404
from django.shortcuts import render
from datetime import datetime
import ujson
from django.http import HttpResponse
from django.template import loader
# from .models import Comprehension, Question, Dictionary, NamedEntityType, Answer, QuestionType
from .models import Comprehension, Question, Dictionary, NamedEntityType, QuestionType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from graphos.sources.simple import SimpleDataSource
from graphos.renderers import flot
import re
import string
from django.db.models import Count
import cogm
import random
from operator import itemgetter
import os
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

def sentences(request):

    comprehensions_list = Comprehension.objects.all()
    comprehensions = [c.ComprehensionsText.split('|') for c in comprehensions_list]

    return render(request,  'qa/sentences.html', {'comprehensions': comprehensions})

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

def exportdataset(request):
    import codecs
    #
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'results/dataset2.txt')
    output_file = codecs.open(file_path, 'a', encoding="utf-8")
    output = ""
    comprehension = Comprehension.objects.all()
    c_count = 0
    q_count = 0
    for c in comprehension:
        c_count += 1
        output += c.ComprehensionTitle + "\n\n" + \
                  c.ComprehensionsText + "\n\n" + \
                  c.ComprehensionTagged + "\n\n\n"
        questions = Question.objects.select_related().filter(Comprehension=c)
        for q in questions:
            q_count += 1
            output += q.QuestionText + "\n"
        output += "\n"
        for q in questions:
            output += q.QuestionTagged + "\n"
        output += "\n ------------------------------------------------- \n"
    import time
    output += "\n\n" + "Comprehensions = " + str(c_count) + "\nQuestions = " + str(q_count) + "\n" + str(time.clock()) + " seconds"
    output_file.writelines(output)
    output_file.close()
    return render(request,  'qa/compdetail.html', {})

def wordcount(request):
    import codecs
    #
    str = ""
    comprehensions = Comprehension.objects.all()
    questions = Question.objects.all()
    for c in comprehensions:
        str += " " + c.ComprehensionsText
    for q in questions:
        str += " " + q.QuestionText
    count = len(set(str.split(' ')))
    import time
    return render(request,  'qa/count.html', {'count': count, 'time': time.clock()})

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
        from nltk.corpus import stopwords

        question = Question.objects.get(pk=question_id)
        question_types = question.QuestionTypeID.all()
        comprehension = Comprehension.objects.get(pk=question.Comprehension_id)

        # Split Question tags string into individual tags
        tag_parts = question.QuestionTagsOnly.split('\\')

        # Find Punctuation Index (W3)
        # punctuations = [i+1 for i, x in enumerate(tag_parts) if x == 'RD_PUNC']
        # punctuation_index = punctuations[-1]

        #Fetch compound words from the dictionary and count their matches against question words
        compound_words = Dictionary.objects.filter(CompoundWord=True)
        question_words = question.QuestionText.split(' ')
        question_compound_words_count = len([match for match in question_words if match in compound_words])

        question_word_tags = [{'word':w, 'tag':t}  for w,t in zip(question_words, tag_parts) if t != "RD_PUNC"]

        all_named_entities = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True)]
        question_named_entities = [m for m in question_words if m in all_named_entities]

        question_named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(dictionary__Word__in=question_named_entities).distinct()]

        question_bag = {'question_word_tags': question_word_tags, 'punctuation_index': 1,
                        'question_compound_words_count': question_compound_words_count,
                        'question_named_entity_types': question_named_entity_types,
                        'question_named_entities': question_named_entities }

        # Break paragraph into sentences
        # sentences = [s.strip() + " |" for s in comprehension.ComprehensionsText.split('|')]
        # del sentences[-1]
        cog_bag = []

        import sentence_formulation as sf

        # sentences = st.who_logic(question.QuestionText, comprehension.ComprehensionsText)
        sentences = sf.formulate(question.QuestionText, comprehension.ComprehensionsText)

        # print sentences
        probable_answers = []
        answers_cog_list = []
        for sentence_index, sentence in enumerate(sentences['sentences']):

            words = sentence.split()

            # sentence_words = [word for word in words if word not in stopwords.words('punjabi')]
            sentence_words = sentence.split()
            # print ",".join(sentence_words)

            sentence_compound_words_count = len([match for match in sentence_words if match in compound_words])
            sentence_named_entities = [m for m in sentence_words if m in all_named_entities]
            sentence_named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(dictionary__Word__in=sentence_named_entities).distinct()]

            # # Find Punctuation Index (W3)
            # punctuations = [iter + 1 for iter, punc in enumerate(sentence_words) if punc == '|']
            # punctuation_index = punctuations[-1]

            del sentence_words[-1]

            # Split Question tags string into individual tags
            sentence_word_tags = []
            for word in sentence_words:
                obj = Dictionary.objects.filter(Word=word).first()
                if obj != None:
                    sentence_word_tags.append({'word': obj.Word, 'tag': obj.WordType})

            sentence_bag = {'sentence_word_tags': sentence_word_tags, 'punctuation_index': 1,
                                'sentence_compound_words_count': sentence_compound_words_count,
                                'sentence_named_entity_types': sentence_named_entity_types,
                                'sentence_named_entities': sentence_named_entities}
            # sentence_tags = []
            # for part in tag_parts:
            #     for p in part:
            #         sentence_tags.append(p)
            #
            # sentence_word_tags = [{'word': w, 'tag': t} for w, t in zip(sentence_words, sentence_tags)]
            # for t in sentence_word_tags:
            #     print t['word'], t['tag']
            #sentence_tags.append('RD_PUNC')


            #print sentence_compound_words_count
            # bonus_value = bonus.get_bonus(question_words, question_named_entity_types, sentence_words,sentence_named_entity_types, sentence_tags)

            # sentence_cog = cogm.calculate_cogm(sentence_words, bonus_value, sentence_compound_words_count, sentence_named_entity_types, sentence_tags, sentence_named_entities)
            cog =  cogm.calculate_cogm(question_bag, sentence_bag)
            distance_similarity = cogm.euclidean_distance_similarity(cog['sentence_cog']['cogX'], cog['sentence_cog']['cogY'],
                                                         cog['question_cog']['cogX'], cog['question_cog']['cogY'])
            cog['euclidean_distance'] = distance_similarity['euclidean_distance']
            cog['similarity'] = distance_similarity['similarity']
            cog['bonus_value'] = cog['sentence_cog']['bonus_value']
            cog['question_cog']['question'] = question.QuestionText
            cog['sentence_cog']['sentence'] = sentence
            cog['matched_bigrams'] = cog['sentence_cog']['matched_bigrams']


            # cog['question_bonus_distance'] = cogm.euclidean_distance(cog['question_cog']['bonus_value']['bonus_x'], cog['question_cog']['bonus_value']['bonus_y'],
            #                                              cog['question_cog']['cogX'], cog['question_cog']['cogY'])
            # cog['sentence_bonus_distance'] = cogm.euclidean_distance(cog['sentence_cog']['bonus_value']['bonus_x'],
            #                                                          cog['sentence_cog']['bonus_value']['bonus_y'],
            #                                                          cog['sentence_cog']['cogX'],
            #                                                          cog['sentence_cog']['cogY'])
            # import math
            # cog['inter_bonus_distance'] = math.sqrt(math.pow(cog['question_bonus_distance'] - cog['sentence_bonus_distance'], 2))


            # probable_answer = {'sentence': sentence, 'sentence_tags': sentence_tags,'cogX': sentence_cog['cogX'], 'cogY': sentence_cog['cogY'], 'cog': [sentence_cog['cogX'], sentence_cog['cogY']],
            #                    'sentence_index': sentence_index + 1, 'lexical_density': sentence_cog['lexical_density'],
            #                    'readability_index': sentence_cog['readability_index'], 'punctuation_index': punctuation_index, 'euclidean_distance': euclidean_distance, 'bonus': bonus_value, 'sentence_cog': sentence_cog }
            # #print probable_answer
            # answers_cog_list.append([sentence_cog['cogX'],sentence_cog['cogY']])
            #print sentence
            cog_bag.append(cog)
            # print cog
        cog_bag = sorted(cog_bag, key=itemgetter('similarity'), reverse=True)

        # import codecs
        #
        # module_dir = os.path.dirname(__file__)  # get current directory
        # file_path = os.path.join(module_dir, 'results.txt')
        # output_file = codecs.open(file_path, 'a', encoding="utf-8")
        # for c in cog_bag:
        #     output = "Question" + "\n" + \
        #              "X1= " + str(c['question_cog']['X1']) + "\n" + \
        #              "Y1= " + str(c['question_cog']['Y1']) + "\n" + \
        #              "X2= " + str(c['question_cog']['X2']) + "\n" + \
        #              "Y2= " + str(c['question_cog']['Y2']) + "\n" + \
        #              "X3= " + str(c['question_cog']['X3']) + "\n" + \
        #              "Y3= " + str(c['question_cog']['Y3']) + "\n" + \
        #              "W1= " + str(c['question_cog']['lexical_density']) + "\n" + \
        #              "W2= " + str(c['question_cog']['readability_index']) + "\n" + \
        #              "W3= " + str(c['question_cog']['q_lex']) + "\n\n" + \
        #              "Sentence" + "\n" + \
        #              "X1= " + str(c['sentence_cog']['X1']) + "\n" + \
        #              "Y1= " + str(c['sentence_cog']['Y1']) + "\n" + \
        #              "X2= " + str(c['sentence_cog']['X2']) + "\n" + \
        #              "Y2= " + str(c['sentence_cog']['Y2']) + "\n" + \
        #              "X3= " + str(c['sentence_cog']['X3']) + "\n" + \
        #              "Y3= " + str(c['sentence_cog']['Y3']) + "\n" + \
        #              "W1= " + str(c['sentence_cog']['lexical_density']) + "\n" + \
        #              "W2= " + str(c['sentence_cog']['readability_index']) + "\n" + \
        #              "W3= " + str(c['sentence_cog']['s_lex']) + "\n\n\n\n"
        #     output_file.writelines(str(output))
        # output_file.close()

        # import codecs
        #
        # module_dir = os.path.dirname(__file__)  # get current directory
        # file_path = os.path.join(module_dir, 'out4.txt')
        # output_file = codecs.open(file_path, 'a', encoding="utf-8")
        # output = re.sub(r'([\'\"\,])', '', cog_bag[0]['question_cog']['question']) + ", (" + \
        #          str(cog_bag[0]['question_cog']['X1']) + " " + \
        #          str(cog_bag[0]['question_cog']['Y1']) + ") " + "(" + str(cog_bag[0]['question_cog']['X2']) + " " + \
        #          str(cog_bag[0]['question_cog']['Y2']) + ") " + "(" + str(cog_bag[0]['question_cog']['X3']) + " " + \
        #          str(cog_bag[0]['question_cog']['Y3']) + "), " + str(cog_bag[0]['question_cog']['lexical_density']) + \
        #          ", " + str(cog_bag[0]['question_cog']['readability_index']) + \
        #          str(cog_bag[0]['question_cog']['q_lex']) + ", (" + str(cog_bag[0]['sentence_cog']['cogX']) + \
        #          " " + str(cog_bag[0]['question_cog']['cogY']) + "), " + str(cog_bag[0]['euclidean_distance']), "\n"
        # output += re.sub(r'([\'\"\,])', '', cog_bag[0]['sentence_cog']['sentence']) + ", (" + \
        #           str(cog_bag[0]['sentence_cog']['X1']) + " " + \
        #           str(cog_bag[0]['sentence_cog']['Y1']) + ") " + "(" + str(cog_bag[0]['sentence_cog']['X2']) + " " + \
        #           str(cog_bag[0]['sentence_cog']['Y2']) + ") " + "(" + str(cog_bag[0]['sentence_cog']['X3']) + " " + \
        #           str(cog_bag[0]['sentence_cog']['Y3']) + "), " + str(cog_bag[0]['sentence_cog']['lexical_density']) + \
        #           ", " + str(cog_bag[0]['sentence_cog']['readability_index']) + \
        #           str(cog_bag[0]['sentence_cog']['s_lex']) + ", (" + str(cog_bag[0]['sentence_cog']['cogX']) + \
        #           " " + str(cog_bag[0]['sentence_cog']['cogY']) + "), " + str(cog_bag[0]['euclidean_distance']), "\n"
        # output_file.writelines(output)
        # output_file.close()

        # cog_bag = sorted(cog_bag, key=itemgetter('euclidean_distance'))
        # cog_bag = sorted(cog_bag, key=itemgetter('bonus_value', 'euclidean_distance'), reverse=True)

        # cog_bag = sorted(cog_bag, key=lambda element: (element['euclidean_distance'], -element['bonus_value']))

        #print answers_cog
        #random.shuffle(answers)

        # nearest_answer = cogm.find_nearest_vector(answers_cog, [question_cog['cogX'], question_cog['cogY']])
        #print nearest_answer



    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    #return render(request,  'qa/questiondetail.html', {'comprehension': comprehension, 'question': question, 'X':[X1,X2,X3], 'Y':[Y1,Y2,Y3], 'graph': graph, 'question_types': question_types})
    # return render(request, 'qa/questiondetail.html', {'comprehension': comprehension, 'question': question, 'q_cog_dump': ujson.dumps(question_cog), 'question_types': question_types, 'answers': answers, 'answers_dump': ujson.dumps(answers)})
    return render(request, 'qa/questiondetail.html',
                  {'comprehension': comprehension, 'question': question, 'cog_bag': cog_bag,
                   'question_types': question_types, \
                   # 'answers': answers, 'answers_dump': ujson.dumps(answers)
                    })

def testing(request, type_id):
    type = QuestionType.objects.get(pk=type_id)

    import codecs
    #
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'results/results_type_'+type_id+'.txt')
    output_file = codecs.open(file_path, 'a', encoding="utf-8")
    type_str = "\n \n" + type.QuestionType + "\n \n"
    output_file.writelines(type_str)

    questions_ids = [q.id for q in Question.objects.filter(QuestionTypeID=type_id)]
    # print questions
    for question_id in questions_ids:
        question = Question.objects.get(pk=question_id)
        comprehension = Comprehension.objects.get(pk=question.Comprehension_id)
        # print comprehension
        # Split Question tags string into individual tags
        tag_parts = question.QuestionTagsOnly.split('\\')

        # Fetch compound words from the dictionary and count their matches against question words
        compound_words = Dictionary.objects.filter(CompoundWord=True)
        question_words = question.QuestionText.split(' ')
        question_compound_words_count = len([match for match in question_words if match in compound_words])

        question_word_tags = [{'word': w, 'tag': t} for w, t in zip(question_words, tag_parts) if t != "RD_PUNC"]

        all_named_entities = [dict.Word for dict in Dictionary.objects.filter(NamedEntity=True)]
        question_named_entities = [m for m in question_words if m in all_named_entities]

        question_named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(
                dictionary__Word__in=question_named_entities).distinct()]

        question_bag = {'question_word_tags': question_word_tags, 'punctuation_index': 1,
                            'question_compound_words_count': question_compound_words_count,
                            'question_named_entity_types': question_named_entity_types,
                            'question_named_entities': question_named_entities}

        cog_bag = []
        import sentence_formulation as sf
        sentences = sf.formulate(question.QuestionText, comprehension.ComprehensionsText)

        probable_answers = []
        answers_cog_list = []
        for sentence_index, sentence in enumerate(sentences['sentences']):
            words = sentence.split()
            sentence_words = sentence.split()
            # print sentence_words
            sentence_compound_words_count = len([match for match in sentence_words if match in compound_words])
            sentence_named_entities = [m for m in sentence_words if m in all_named_entities]
            sentence_named_entity_types = [ne.name for ne in NamedEntityType.objects.filter(
                    dictionary__Word__in=sentence_named_entities).distinct()]

            del sentence_words[-1]
            # punctuations = [iter + 1 for iter, punc in enumerate(sentence_words) if punc == u'|']
            # print punctuations
            # punctuation_index = punctuations[-1]

            sentence_word_tags = []
            for word in sentence_words:
                obj = Dictionary.objects.filter(Word=word).first()
                if obj != None:
                    sentence_word_tags.append({'word': obj.Word, 'tag': obj.WordType})

            sentence_bag = {'sentence_word_tags': sentence_word_tags, 'punctuation_index': 1,
                                'sentence_compound_words_count': sentence_compound_words_count,
                                'sentence_named_entity_types': sentence_named_entity_types,
                                'sentence_named_entities': sentence_named_entities}
            cog = cogm.calculate_cogm(question_bag, sentence_bag)
            distance_similarity = cogm.euclidean_distance_similarity(cog['sentence_cog']['cogX'], cog['sentence_cog']['cogY'],
                                                             cog['question_cog']['cogX'], cog['question_cog']['cogY'])
            cog['euclidean_distance'] = distance_similarity['euclidean_distance']
            cog['similarity'] = distance_similarity['similarity']
            cog['bonus_value'] = cog['sentence_cog']['bonus_value']
            cog['question_cog']['question'] = question.QuestionText
            cog['sentence_cog']['sentence'] = sentence
            cog['matched_bigrams'] = cog['sentence_cog']['matched_bigrams']

            cog_bag.append(cog)

        cog_bag = sorted(cog_bag, key=itemgetter('similarity'), reverse=True)

        try:
            if len(cog_bag) > 0:
                output = re.sub(r'([\'\"\,])', '', cog_bag[0]['question_cog']['question']) + ", (" + \
                        str(cog_bag[0]['question_cog']['X1']) + " " + \
                        str(cog_bag[0]['question_cog']['Y1']) + ") " + "(" + str(cog_bag[0]['question_cog']['X2']) + " " + \
                        str(cog_bag[0]['question_cog']['Y2']) + ") " + "(" + str(cog_bag[0]['question_cog']['X3']) + " " + \
                        str(cog_bag[0]['question_cog']['Y3']) + "), " + str(cog_bag[0]['question_cog']['lexical_density']) + \
                        ", " + str(cog_bag[0]['question_cog']['readability_index']) + \
                        str(cog_bag[0]['question_cog']['q_lex']) + ", (" + str(cog_bag[0]['sentence_cog']['cogX']) + \
                        " " + str(cog_bag[0]['question_cog']['cogY']) + "), " + str(cog_bag[0]['euclidean_distance']) + ", " + \
                        str(cog_bag[0]['similarity']), "\n"
                output += re.sub(r'([\'\"\,])', '', cog_bag[0]['sentence_cog']['sentence']) + ", (" + \
                        str(cog_bag[0]['sentence_cog']['X1']) + " " + \
                        str(cog_bag[0]['sentence_cog']['Y1']) + ") " + "(" + str(cog_bag[0]['sentence_cog']['X2']) + " " + \
                        str(cog_bag[0]['sentence_cog']['Y2']) + ") " + "(" + str(cog_bag[0]['sentence_cog']['X3']) + " " + \
                        str(cog_bag[0]['sentence_cog']['Y3']) + "), " + str(cog_bag[0]['sentence_cog']['lexical_density']) + \
                        ", " + str(cog_bag[0]['sentence_cog']['readability_index']) + \
                        str(cog_bag[0]['sentence_cog']['s_lex']) + ", (" + str(cog_bag[0]['sentence_cog']['cogX']) + \
                        " " + str(cog_bag[0]['sentence_cog']['cogY']) + "), " + str(cog_bag[0]['euclidean_distance']) + ", " + \
                        str(cog_bag[0]['similarity']), "\n"
                output_file.writelines(output)
        except (IndexError, ValueError):
            pass
        # print output_list
    output_file.close()


    # types = QuestionType.objects.annotate(count=Count('questiontypes')).order_by('-count').values('id', 'count')
    return render(request, 'qa/testing.html', {})