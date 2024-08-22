from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class SubscriptionForm(forms.Form):
    DURATION_CHOICES = [
        ('1_month', '1 Month'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ]
    duration = forms.ChoiceField(choices=DURATION_CHOICES)