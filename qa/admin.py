from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
import re
#from django.forms import ModelForm

# Register your models here.

#from .models import Question, Answer, AnswerType, QuestionType, Comprehension, Dictionary, Patterns, IndependentQuestion, IndependentQuestionSet, DictionarySet, NamedEntityType
from .models import Question, QuestionType, Comprehension, Dictionary, Patterns, IndependentQuestion, IndependentQuestionSet, DictionarySet, NamedEntityType

class ComprehensionForm(forms.ModelForm):
    model = Comprehension

class QuestionForm(forms.ModelForm):
    model = Question

    def clean(self):
        cleaned_data = self.cleaned_data

        QTaggsOnly = re.sub(r'([^A-Z_a-z\\])', '', cleaned_data['QuestionTagged'].strip())
        cleaned_data['QuestionTagsOnly'] = QTaggsOnly
        return cleaned_data

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['QuestionTypeID', 'Comprehension', 'LastUpdate']
    search_fields = ['QuestionText']
    list_display = ('QuestionText', 'LastUpdate')
    form = QuestionForm

class QuestionInline(admin.TabularInline):  # Similar to book in example github page
    fields = ('QuestionText', 'QuestionTypeID','QuestionTagged')
    model = Question
    extra = 0

# class AnswerInline(admin.TabularInline):   # Similar to Press in github page
#     model = Answer
#     #formset = ComprehensionFormSet
#    # extra = 2

# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('AnswerText', 'Comprehension', 'SentenceIndex', 'LastUpdate')
#     list_filter = ['Comprehension']
#     search_fields = ['AnswerText']

class ComprehensionAdmin(admin.ModelAdmin):
    search_fields = ['ComprehensionsText']
    form = ComprehensionForm

    fieldsets = [
        ('Main', {'fields': ['ComprehensionTitle','ComprehensionsText','ComprehensionTagged','ComprehensionTagsOnly']}),
        ('Additional Info', {'fields': ['ComprehensionsRemarks'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
    list_display = ('ComprehensionTitle', 'LastUpdate')
    list_per_page = 20

class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('QuestionType', 'QuestionTypeDesc')

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
# admin.site.register(AnswerType)
# admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comprehension, ComprehensionAdmin)

class DictionaryAdmin(admin.ModelAdmin):
    search_fields = ['WordType', 'Word']
    list_filter = ['WordType', 'NamedEntity']
    list_display = ['Word', 'WordType', 'StemmedWord', 'LastUpdate']
    fields = ('Word', 'WordType', 'NamedEntity', 'NamedEntityTypeID', 'CompoundWord')

class DictionaryInline(admin.TabularInline):
    model = Dictionary
    extra = 0

class DictionaryInlineforNE(admin.TabularInline):
    model = Dictionary.NamedEntityTypeID.through
    extra = 1
    verbose_name = "Word"


class DictionarySetAdmin(admin.ModelAdmin):
    inlines = [DictionaryInline]

class NamedEntityTypeAdmin(admin.ModelAdmin):
    inlines = [DictionaryInlineforNE]

admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(DictionarySet, DictionarySetAdmin)
admin.site.register(Patterns)


class IndependentQuestionInline(admin.TabularInline):  # Similar to book in example github page
    model = IndependentQuestion
    extra = 86

class IndependentQuestionAdmin(admin.ModelAdmin):
    list_filter = ['QuestionTypeID', 'LastUpdate']
    search_fields = ['QuestionText']
    list_display = ('QuestionText', 'LastUpdate')

class QuestionSetAdmin(admin.ModelAdmin):
    inlines = [IndependentQuestionInline]

admin.site.register(IndependentQuestion, IndependentQuestionAdmin)
admin.site.register(IndependentQuestionSet, QuestionSetAdmin)
admin.site.register(NamedEntityType, NamedEntityTypeAdmin)