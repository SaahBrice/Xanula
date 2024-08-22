from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
import string
import random
from accounts.models import User


def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    unique_code = models.CharField(default=generate_unique_code,max_length=20, unique=True)

    def __str__(self):
        return self.name

class Workbook(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    workbook = models.ForeignKey(Workbook, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.workbook.title} - {self.title}"

class Quiz(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple', 'Multiple Choice'),
        ('single', 'Single Choice'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    date_attempted = models.DateTimeField(auto_now_add=True)
    date_attempted = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'quiz']

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title}"

class QuestionResponse(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=True)
    response_time = models.DurationField(default=timedelta(seconds=0))

    class Meta:
        unique_together = ['quiz_attempt', 'question']



class PastExamPaper(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    pdf_file = models.FileField(upload_to='past_exam_papers/')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.year}"

class PastExamQuestion(models.Model):
    exam_paper = models.ForeignKey(PastExamPaper, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField()
    video_solution_url = models.URLField(help_text="YouTube video URL for the solution", blank=True)
    written_solution = models.FileField(upload_to='past_exam_solutions/pdfs/')

    class Meta:
        unique_together = ['exam_paper', 'question_number']

    def __str__(self):
        return f"{self.exam_paper.name} - Question {self.question_number}"

class ExplanationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('answered', 'Answered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(PastExamQuestion, on_delete=models.CASCADE)
    request_text = models.TextField()
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Request for {self.question} by {self.user.username}"



class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient or 'All'}: {self.message[:50]}..."