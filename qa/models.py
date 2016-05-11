from __future__ import unicode_literals, division
from django.db import models
from django.utils import timezone
import datetime
import re
import stemmer
import ujson


# Create your models here.

class Comprehension(models.Model):
    ComprehensionTitle = models.CharField(max_length=100, verbose_name='Comprehension Title', unique=True)
    ComprehensionsText = models.TextField(verbose_name='Text')
    ComprehensionTagged = models.TextField(verbose_name='pos tagged text', null=True, blank=True)
    ComprehensionTagsOnly = models.TextField(verbose_name='tags only', null=True, blank=True)
    ComprehensionsRemarks = models.CharField(max_length=400, verbose_name='Remarks for this Comprehension', null=True,  blank=True)
    LastUpdate = models.DateTimeField("Last Updated", auto_now=True)
    def __unicode__(self):
        return self.ComprehensionTitle
    def was_published_recently(self):
        return self.LastUpdate >= timezone.now() - datetime.timedelta(1)

    def save(self, *args, **kwargs):
        #overrides the default save function to split the comprehension paragraph into sentences and adds them as probable answers

        CTaggsOnly = re.sub(r'([^A-Z_a-z\\])', '', self.ComprehensionTagged.strip())
        self.ComprehensionTagsOnly = CTaggsOnly[1:]

        #Splits the tagged comprehension into Word\WordType pairs and inserts them into dictionary
        words = re.sub(r'([\'\"])', '', self.ComprehensionTagged)
        wordslist = words.split(' ')
        list = [word.split('\\') for word in wordslist if word]

        for pair in list:
            #p, created = Dictionary.objects.get_or_create(Word = pair[0], WordType = pair[1])
            try:
                p = Dictionary.objects.get(Word = pair[0])
            except Dictionary.DoesNotExist:
                p = Dictionary(Word = pair[0], WordType = pair[1])
            p.save()

        #Splits the main comprehension passage into sentences of probable answers

        # compseperator = "|"
        # Comp = re.sub(r'([\'\"])', '', self.ComprehensionsText.strip() )
        # AnswerList = [e.strip() + compseperator for e in Comp.split(compseperator) if e != ""]
        #
        # tagseperator = "|\RD_PUNC"
        # TaggedComp = self.ComprehensionTagged.strip()
        # TaggedAnswerList = [re.sub(r'([^A-Z_a-z\\])', '', f.strip()) + re.sub(r'([\|])', '', tagseperator) for f in TaggedComp.split(tagseperator) if f != ""]
        #
        # for i,(sentence, taggedanswer) in enumerate(zip(AnswerList, TaggedAnswerList)):
        #     try:
        #         obj, created = Answer.objects.get_or_create(AnswerText = sentence, AnswerTagsOnly = taggedanswer, Comprehension = self, SentenceIndex = i+1)
        #     except Exception as e:
        #        print e
        #     #d = Answer.objects.update_or_create(AnswerTagsOnly = taggedanswer, ComprehensionAnswer = self, SentenceIndex = i+1)

        super(Comprehension, self).save(*args, **kwargs)

class QuestionType(models.Model):
    QuestionType = models.CharField(max_length=100, verbose_name='Question Type')
    QuestionTypeDesc = models.CharField(max_length=200, verbose_name='Description of Question Type')
    def __unicode__(self):
        return self.QuestionType

class Question(models.Model):
    QuestionText = models.CharField(max_length=500, verbose_name='Question Text')
    QuestionTypeID = models.ManyToManyField(QuestionType, verbose_name='Question Type', related_name='questiontypes')
    QuestionTagged = models.CharField(max_length=500, verbose_name='pos tagged text', null=True, blank=True)
    QuestionTagsOnly = models.CharField(max_length=500, verbose_name='pos tags', null=True, blank=True)
    Comprehension = models.ForeignKey(Comprehension, verbose_name='comprehension', null=True)
    # LexicalDensity = models.FloatField(null=True, blank=True)
    # ReadabilityIndex = models.FloatField(null=True, blank=True)
    # PunctuationIndex = models.CharField(max_length=200, verbose_name='punctuation index', default='0', null=True)
    # cogX = models.FloatField(default=0, null=True)
    # cogY = models.FloatField(default=0, null=True)
    # center_of_gravity = models.FloatField(default=0,null=True)
    QuestionRemarks = models.CharField(max_length=500, verbose_name='remarks', null=True, blank=True)
    LastUpdate = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.QuestionText
    def was_published_recently(self):
        return self.LastUpdate >= timezone.now() - datetime.timedelta(1)

    def save(self, *args, **kwargs):

        QTaggsOnly = re.sub(r'([^A-Z_a-z\\])', '', self.QuestionTagged.strip())
        self.QuestionTagsOnly = QTaggsOnly[1:]

        words = re.sub(r'([\'\"])', '', self.QuestionTagged)
        wordslist = words.split(' ')
        list = [word.split('\\') for word in wordslist if word]

        for pair in list:
            try:
                p = Dictionary.objects.get(Word = pair[0])
            except Dictionary.DoesNotExist:
                p = Dictionary(Word = pair[0], WordType = pair[1])
            p.save()

        # parts = self.QuestionTagsOnly.split('\\')
        #
        # punctuations = [i+1 for i, x in enumerate(parts) if x == 'RD_PUNC']
        # self.PunctuationIndex = ujson.dumps(punctuations)
        #
        # Nlex = parts.count('N_NN') + parts.count('N_NNP') + parts.count('V_VM') + parts.count('V_VM_VNF') + parts.count('V_VM_VINF') + parts.count('V_VM_VNG') + parts.count('V_VAUX') + parts.count('JJ') + parts.count('RB')
        # self.LexicalDensity = Nlex / len(parts)
        super(Question, self).save(*args, **kwargs)


class IndependentQuestionSet(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class IndependentQuestion(models.Model):
    QuestionText = models.CharField(max_length=500, verbose_name='Question Text')
    QuestionTypeID = models.ManyToManyField(QuestionType, verbose_name='Question Type')
    QuestionTagged = models.CharField(max_length=500, verbose_name='pos tagged text', null=True, blank=True)
    QuestionTagsOnly = models.CharField(max_length=500, verbose_name='pos tags', null=True, blank=True)
    QuestionRemarks = models.CharField(max_length=500, verbose_name='remarks', null=True, blank=True)
    QuestionSet = models.ForeignKey(IndependentQuestionSet, verbose_name='question set', null=True)
    LastUpdate = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.QuestionText
    def was_published_recently(self):
        return self.LastUpdate >= timezone.now() - datetime.timedelta(1)

    def save(self, *args, **kwargs):
        #overrides the default save function to remove punjabi and save tagsonly

        TaggsOnly = re.sub(r'([^A-Z_a-z\\])', '', self.QuestionTagged.strip())
        self.QuestionTagsOnly = TaggsOnly[1:]

        super(IndependentQuestion, self).save(*args, **kwargs)

# class AnswerType(models.Model):
#     AnswerType = models.CharField(max_length=100, verbose_name='Answer Type')
#     AnswerTypeDesc = models.CharField(max_length=200, verbose_name='Description of Answer Type')
#     def __unicode__(self):
#         return self.AnswerType
#
# class Answer(models.Model):
#     ##AnswerTypeID = models.ForeignKey(AnswerType, verbose_name='Answer Type')
#     AnswerText = models.CharField(max_length=500, verbose_name='Answer Text')
#     AnswerTypeID = models.ManyToManyField(AnswerType, verbose_name='Answer Type', blank=True)
#     AnswerTagsOnly = models.CharField(max_length=500, verbose_name='pos tags', null=True, blank=True)
#     Comprehension = models.ForeignKey(Comprehension, verbose_name='Comprehension', null=True)
#     SentenceIndex = models.IntegerField(default = 0)
#     LexicalDensity = models.FloatField()
#     ReadabilityIndex = models.FloatField()
#     PunctuationIndex = models.CharField(max_length=200, verbose_name='punctuation index', default='0')
#     cogX = models.FloatField(default=0)
#     cogY = models.FloatField(default=0)
#     center_of_gravity = models.FloatField(default=0)
#     AnswerRemarks = models.CharField(max_length=500, verbose_name='Remarks', blank=True)
#     LastUpdate = models.DateTimeField(auto_now=True)
#     def __unicode__(self):
#         return self.AnswerText
#
#     def save(self, *args, **kwargs):
#         parts = self.AnswerTagsOnly.split('\\')
#
#         punctuations = [i+1 for i, x in enumerate(parts) if x == 'RD_PUNC']
#         self.PunctuationIndex = ujson.dumps(punctuations)
#
#         Nlex = parts.count('N_NN') + parts.count('N_NNP') + parts.count('V_VM') + parts.count('V_VM_VNF') + parts.count('V_VM_VINF') + parts.count('V_VM_VNG') + parts.count('V_VAUX') + parts.count('JJ') + parts.count('RB')
#         self.LexicalDensity = Nlex / len(parts)
#         super(Answer, self).save(*args, **kwargs)

class DictionarySet(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class NamedEntityType(models.Model):
    name = models.CharField(max_length=100)
    punjabi_name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Dictionary(models.Model):
    Word= models.CharField(max_length=200, verbose_name='word', null=False, blank=False, default="none"  )
    WordType = models.CharField(max_length=200, verbose_name='word type', null=True, blank=False)
    StemmedWord = models.CharField(max_length=200, verbose_name='stemmed word', null=True)
    NamedEntity = models.BooleanField(default=False, verbose_name='named entity')
    NamedEntityTypeID = models.ManyToManyField(NamedEntityType, verbose_name='named entity type', blank=True)
    CompoundWord = models.BooleanField(default=False, verbose_name='complex word')
    DictionarySet = models.ForeignKey(DictionarySet, verbose_name='dictionary set', null=True)
    LastUpdate = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('Word', 'WordType')
    def __unicode__(self):
        return self.Word
    class Meta:
        verbose_name_plural = "Dictionary"
    def save(self, *args, **kwargs):

        self.StemmedWord = stemmer.stem(self.Word)

        super(Dictionary, self).save(*args, **kwargs)

class Patterns(models.Model):
    QuestionTypeID = models.ForeignKey(QuestionType, verbose_name='Question Type')
    # AnswerTypeID = models.ForeignKey(AnswerType, verbose_name='Answer Type')
    PatternName	= models.CharField(max_length=100, verbose_name='Pattern Name')
    PatternDesc = models.CharField(max_length=350, verbose_name='Pattern Description')
    PatternRegularExpression = models.CharField(max_length=350, verbose_name='Pattern Regular Expression')
    def __unicode__(self):
        return self.PatternName
    class Meta:
        verbose_name = 'pattern'
        verbose_name_plural = 'patterns'

class Statistics(models.Model):
    StatisticsTitle	= models.CharField(max_length=200, verbose_name='Statistics Title')
    StatisticsX = models.CharField(max_length=10, verbose_name='Statistics X')
    StatisticsY = models.CharField(max_length=10, verbose_name='Statistics Y')
    def __unicode__(self):
        return self.StatisticsTitle