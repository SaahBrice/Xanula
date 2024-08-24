from django import forms
from core.models import ExplanationRequest, Notification, Quiz, Workbook, Subject, PastExamPaper
from subscriptions.models import Subscription, SubscriptionPlan
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkbookForm(forms.ModelForm):
    class Meta:
        model = Workbook
        fields = ['title', 'subject', 'author', 'image', 'is_paid']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class PastExamPaperForm(forms.ModelForm):
    class Meta:
        model = PastExamPaper
        fields = ['name', 'subject', 'image', 'year', 'pdf_file', 'is_paid']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        
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


class NotificationForm(forms.ModelForm):
    send_to_all = forms.BooleanField(required=False, initial=False, label="Send to all students")
    recipient = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False), required=False)

    class Meta:
        model = Notification
        fields = ['message', 'recipient', 'send_to_all']

    def clean(self):
        cleaned_data = super().clean()
        send_to_all = cleaned_data.get('send_to_all')
        recipient = cleaned_data.get('recipient')

        if not send_to_all and not recipient:
            raise forms.ValidationError("You must either select a recipient or choose to send to all students.")

        if send_to_all and recipient:
            raise forms.ValidationError("You can't select a recipient and send to all students at the same time.")

        return cleaned_data
    
