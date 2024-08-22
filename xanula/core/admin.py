from django.contrib import admin

from .models import Subject, Author, Workbook, Chapter, Quiz, Question, Choice



class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class WorkbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'author', 'is_paid')
    list_filter = ('subject', 'author', 'is_paid')
    search_fields = ('title', 'subject__name', 'author__name')
    inlines = [ChapterInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter')
    list_filter = ('chapter__workbook__subject',)
    search_fields = ('title', 'chapter__title')
    inlines = [QuestionInline]

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type')
    list_filter = ('quiz__chapter__workbook__subject', 'question_type')
    search_fields = ('text', 'quiz__title')
    inlines = [ChoiceInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_code')



admin.site.register(Subject)

admin.site.register(Workbook, WorkbookAdmin)
admin.site.register(Chapter)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)