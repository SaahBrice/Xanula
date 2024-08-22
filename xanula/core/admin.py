from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html
from .models import ExplanationRequest, PastExamPaper, PastExamQuestion, Subject, Author, Workbook, Chapter, Quiz, Question, Choice



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








@admin.register(PastExamPaper)
class PastExamPaperAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'year', 'is_paid')
    list_filter = ('subject', 'year', 'is_paid')
    search_fields = ('name', 'subject__name')

@admin.register(PastExamQuestion)
class PastExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('exam_paper', 'question_number')
    list_filter = ('exam_paper__subject', 'exam_paper__year')

@admin.register(ExplanationRequest)
class ExplanationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at', 'status_colored', 'admin_actions')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'question__exam_paper__name')
    readonly_fields = ('user', 'question', 'request_text', 'created_at')
    fields = ('user', 'question', 'request_text', 'created_at', 'admin_response', 'status')

    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'answered': 'green',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors[obj.status],
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'

    def admin_actions(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Respond</a>',
                f'/admin/core/explanationrequest/{obj.id}/change/'
            )
        return '-'
    admin_actions.short_description = 'Actions'

    def save_model(self, request, obj, form, change):
        if 'admin_response' in form.changed_data:
            obj.responded_at = timezone.now()
            obj.status = 'answered'
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['pending_requests'] = ExplanationRequest.objects.filter(status='pending').count()
        return super().changelist_view(request, extra_context=extra_context)

class PendingExplanationRequestFilter(admin.SimpleListFilter):
    title = 'pending requests'
    parameter_name = 'pending'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(status='pending')
        if self.value() == 'no':
            return queryset.exclude(status='pending')




admin.site.register(Subject)

admin.site.register(Workbook, WorkbookAdmin)
admin.site.register(Chapter)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)