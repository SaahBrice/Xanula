from datetime import timedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .models import Author, ExplanationRequest, Notification, PastExamPaper, PastExamQuestion, Subject, Workbook, Chapter, Quiz, Question, Choice, QuizAttempt, QuestionResponse
from django import forms
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .ai_utils import get_ai_explanation
from .models import QuestionResponse
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count, Avg


class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:student_home')
        return super().get(request, *args, **kwargs)

class StudentHomeView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'core/student_home.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.prefetch_related('workbook_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_exam_papers'] = PastExamPaper.objects.order_by('-id')[:5]  # Get 5 most recent exam papers
        context['recent_explanation_requests'] = ExplanationRequest.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return context



class WorkbookListView(LoginRequiredMixin, ListView):
    model = Workbook
    template_name = 'core/workbook_list.html'
    context_object_name = 'workbooks'

    def get_queryset(self):
        return Workbook.objects.filter(subject_id=self.kwargs['subject_id']).select_related('author')

class WorkbookDetailView(LoginRequiredMixin, DetailView):
    model = Workbook
    template_name = 'core/workbook_detail.html'
    context_object_name = 'workbook'

    def get_queryset(self):
        return super().get_queryset().select_related('subject', 'author').prefetch_related('chapter_set')



class QuizView(LoginRequiredMixin, FormView):
    template_name = 'core/quiz.html'
    form_class = forms.Form

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        for question in self.quiz.question_set.all():
            field_name = f'question_{question.id}'
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            if question.question_type == 'multiple':
                form.fields[field_name] = forms.MultipleChoiceField(
                    choices=choices, widget=forms.CheckboxSelectMultiple, required=False, label=question.text, 
                )
            else:
                form.fields[field_name] = forms.ChoiceField(
                    choices=choices, widget=forms.RadioSelect, required=False, label=question.text,
                )
        return form




    def form_valid(self, form):
        with transaction.atomic():
            quiz_attempt, created = QuizAttempt.objects.get_or_create(
                user=self.request.user,
                quiz=self.quiz,
                defaults={'score': 0}
            )

            # Delete previous responses if this is a retry
            if not created:
                QuestionResponse.objects.filter(quiz_attempt=quiz_attempt).delete()

            correct_answers = 0
            total_questions = self.quiz.question_set.count()

            for question in self.quiz.question_set.all():
                field_name = f'question_{question.id}'
                selected_choice_ids = form.cleaned_data.get(field_name, [])
                if not isinstance(selected_choice_ids, list):
                    selected_choice_ids = [selected_choice_ids]
                
                if selected_choice_ids:
                    choice_id = selected_choice_ids[0]
                    choice = Choice.objects.get(id=choice_id)
                    response_time = form.cleaned_data.get(f'response_time_{question.id}', 0)
                    QuestionResponse.objects.create(
                        quiz_attempt=quiz_attempt,
                        question=question,
                        selected_choice=choice,
                        response_time=timedelta(seconds=response_time)
                    )
                    
                    if question.question_type == 'multiple':
                        if set(selected_choice_ids) == set(question.choice_set.filter(is_correct=True).values_list('id', flat=True)):
                            correct_answers += 1
                            
                    else:
                        if choice.is_correct:
                            correct_answers += 1
                
            quiz_attempt.score = (correct_answers / total_questions) * 100
            quiz_attempt.save()

        return redirect(reverse('core:quiz_result', kwargs={'attempt_id': quiz_attempt.id}))



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.quiz
        context['questions'] = self.quiz.question_set.all()
        return context

class QuizResultView(LoginRequiredMixin, DetailView):
    model = QuizAttempt
    template_name = 'core/quiz_result.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'

    def get_queryset(self):
        return super().get_queryset().select_related('quiz').prefetch_related(
            'questionresponse_set__question__choice_set',
            'questionresponse_set__selected_choice'
        )


@login_required
@require_POST
def get_explanation(request):
    response_id = request.POST.get('response_id')
    response = QuestionResponse.objects.select_related('question').get(id=response_id)
    
    correct_answer = response.question.choice_set.filter(is_correct=True).first().text
    explanation = get_ai_explanation(
        response.question.text,
        correct_answer,
        response.selected_choice.text
    )
    
    return JsonResponse({'explanation': explanation})



class AuthorDashboardView(DetailView):
    model = Author
    template_name = 'core/author_dashboard.html'
    context_object_name = 'author'

    def get_object(self):
        unique_code = self.kwargs['unique_code']
        return get_object_or_404(Author, unique_code=unique_code)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        workbooks = Workbook.objects.filter(author=author)
        
        context['workbooks'] = workbooks
        context['total_workbooks'] = workbooks.count()
        
        quiz_count = Sum('chapter__quiz__id')
        context['total_quizzes'] = workbooks.aggregate(total=quiz_count)['total'] or 0
        
        attempts_count = Count('chapter__quiz__quizattempt')
        context['total_attempts'] = workbooks.aggregate(total=attempts_count)['total'] or 0
        
        # Calculate revenue (assuming 1 Xan per attempt)
        context['total_revenue'] = context['total_attempts']
        
        return context
    

class AuthorLoginView(View):
    template_name = 'core/author_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        unique_code = request.POST.get('unique_code')
        if unique_code:
            try:
                author = Author.objects.get(unique_code=unique_code)
                return redirect('core:author_dashboard', unique_code=unique_code)
            except Author.DoesNotExist:
                return render(request, self.template_name, {'error': 'Invalid unique code'})
        else:
            return render(request, self.template_name, {'error': 'Please enter a unique code'})



def workbook_analytics(request, workbook_id):
    workbook = Workbook.objects.get(id=workbook_id)
    
    # Performance over time
    attempts_over_time = QuizAttempt.objects.filter(
        quiz__chapter__workbook=workbook
    ).annotate(
        date=TruncDate('date_attempted')
    ).values('date').annotate(
        avg_score=Avg('score'),
        attempt_count=Count('id')
    ).order_by('date')

    # Most challenging questions
    challenging_questions = QuestionResponse.objects.filter(
        quiz_attempt__quiz__chapter__workbook=workbook,
        is_correct=False
    ).values('question__text').annotate(
        incorrect_count=Count('id')
    ).order_by('-incorrect_count')[:5]

    # Average completion time per chapter
    completion_time = QuizAttempt.objects.filter(
        quiz__chapter__workbook=workbook
    ).values('quiz__chapter__title').annotate(
        avg_time=Avg('questionresponse__response_time')
    )

    return JsonResponse({
        'attempts_over_time': list(attempts_over_time),
        'challenging_questions': list(challenging_questions),
        'completion_time': list(completion_time)
    })




class PastExamPaperListView(LoginRequiredMixin, ListView):
    model = PastExamPaper
    template_name = 'core/past_exam_paper_list.html'
    context_object_name = 'exam_papers'
    paginate_by = 12  # Show 12 exam papers per page

    def get_queryset(self):
        queryset = super().get_queryset()
        subject = self.request.GET.get('subject')
        year = self.request.GET.get('year')
        if subject:
            queryset = queryset.filter(subject__name=subject)
        if year:
            queryset = queryset.filter(year=year)
        return queryset.order_by('-year', 'subject__name', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['years'] = PastExamPaper.objects.values_list('year', flat=True).distinct().order_by('-year')
        return context



class PastExamPaperDetailView(LoginRequiredMixin, DetailView):
    model = PastExamPaper
    template_name = 'core/past_exam_paper_detail.html'
    context_object_name = 'exam_paper'

    def get(self, request, *args, **kwargs):
        exam_paper = self.get_object()
        if exam_paper.is_paid and not request.user.has_active_subscription():
            return HttpResponseForbidden("You must have an active subscription to access this content.")
        return super().get(request, *args, **kwargs)


class DownloadSolutionView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question = get_object_or_404(PastExamQuestion, id=question_id)
        if question.exam_paper.is_paid and not request.user.request.user.has_active_subscription():
            return HttpResponseForbidden("You must have an active subscription to access this content.")
        
        response = HttpResponse(question.written_solution, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{question.exam_paper.name}_Q{question.question_number}_solution.pdf"'
        return response




class ExplanationRequestView(LoginRequiredMixin, CreateView):
    model = ExplanationRequest
    fields = ['request_text']
    template_name = 'core/explanation_request_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = get_object_or_404(PastExamQuestion, pk=self.kwargs['question_id'])
        form.instance.status = 'pending'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:explanation_request_detail', kwargs={'pk': self.object.pk})

class ExplanationRequestDetailView(LoginRequiredMixin, DetailView):
    model = ExplanationRequest
    template_name = 'core/explanation_request_detail.html'
    context_object_name = 'request'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'core/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ) | Notification.objects.filter(is_global=True).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        Notification.objects.filter(is_global=True, is_read=False).update(is_read=True)
        return response