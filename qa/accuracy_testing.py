from qa.models import Comprehension, Question, Dictionary, NamedEntityType, QuestionType
import os
import cogm
from operator import itemgetter
import re


def get_results():
    question_types_list = QuestionType.objects.all()

    for type in question_types_list:
        import codecs
        #
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'out4.txt')
        output_file = codecs.open(file_path, 'a', encoding="utf-8")

        questions_ids = [q.id for q in Question.objects.filter(QuestionTypeID=type)]
        output_list = ""
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

            punctuations = [i + 1 for i, x in enumerate(tag_parts) if x == 'RD_PUNC']
            punctuation_index = punctuations[-1]
            question_bag = {'question_word_tags': question_word_tags, 'punctuation_index': punctuation_index,
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
                euclidean_distance = cogm.euclidean_distance(cog['sentence_cog']['cogX'], cog['sentence_cog']['cogY'],
                                                             cog['question_cog']['cogX'], cog['question_cog']['cogY'])
                cog['euclidean_distance'] = euclidean_distance
                cog['bonus_value'] = cog['sentence_cog']['bonus_value']
                cog['question_cog']['question'] = question.QuestionText
                cog['sentence_cog']['sentence'] = sentence
                cog['matched_bigrams'] = cog['sentence_cog']['matched_bigrams']

                cog_bag.append(cog)

            cog_bag = sorted(cog_bag, key=itemgetter('euclidean_distance'))

            try:
                if len(cog_bag) > 0:
                    output = re.sub(r'([\'\"\,])', '', cog_bag[0]['question_cog']['question']) + ", (" + \
                             str(cog_bag[0]['question_cog']['X1']) + " " + \
                             str(cog_bag[0]['question_cog']['Y1']) + ") " + "(" + str(cog_bag[0]['question_cog']['X2']) + " " + \
                             str(cog_bag[0]['question_cog']['Y2']) + ") " + "(" + str(cog_bag[0]['question_cog']['X3']) + " " + \
                             str(cog_bag[0]['question_cog']['Y3']) + "), " + str(cog_bag[0]['question_cog']['lexical_density']) + \
                             ", " + str(cog_bag[0]['question_cog']['readability_index']) + \
                             str(cog_bag[0]['question_cog']['q_lex']) + ", (" + str(cog_bag[0]['sentence_cog']['cogX']) + \
                             " " + str(cog_bag[0]['question_cog']['cogY']) + "), " + str(cog_bag[0]['euclidean_distance']), "\n"
                    output += re.sub(r'([\'\"\,])', '', cog_bag[0]['sentence_cog']['sentence']) + ", (" + \
                              str(cog_bag[0]['sentence_cog']['X1']) + " " + \
                              str(cog_bag[0]['sentence_cog']['Y1']) + ") " + "(" + str(cog_bag[0]['sentence_cog']['X2']) + " " + \
                              str(cog_bag[0]['sentence_cog']['Y2']) + ") " + "(" + str(cog_bag[0]['sentence_cog']['X3']) + " " + \
                              str(cog_bag[0]['sentence_cog']['Y3']) + "), " + str(cog_bag[0]['sentence_cog']['lexical_density']) + \
                              ", " + str(cog_bag[0]['sentence_cog']['readability_index']) + \
                              str(cog_bag[0]['sentence_cog']['s_lex']) + ", (" + str(cog_bag[0]['sentence_cog']['cogX']) + \
                              " " + str(cog_bag[0]['sentence_cog']['cogY']) + "), " + str(cog_bag[0]['euclidean_distance']), "\n"
                    output_list += str(output)
            except (IndexError, ValueError):
                pass
        # print output_list
        output_file.writelines(output_list)
        output_file.close()
    return "Completed"
