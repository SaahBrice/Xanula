from django import forms
from core.models import ExplanationRequest, Workbook, Subject, PastExamPaper
from subscriptions.models import Subscription, SubscriptionPlan
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkbookForm(forms.ModelForm):
    class Meta:
        model = Workbook
        fields = ['title', 'subject', 'author', 'is_paid']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class PastExamPaperForm(forms.ModelForm):
    class Meta:
        model = PastExamPaper
        fields = ['name', 'subject', 'year', 'pdf_file', 'is_paid']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'start_date', 'end_date', 'is_active']

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'duration_days', 'price', 'description']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active']
    


class ExplanationResponseForm(forms.ModelForm):
    class Meta:
        model = ExplanationRequest
        fields = ['admin_response']
        widgets = {
            'admin_response': forms.Textarea(),
        }