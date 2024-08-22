from datetime import timezone
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from dateutil.relativedelta import relativedelta
from .forms import SubscriptionForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard:dashboard')
            else:
                return redirect('core:student_home')
        else:
            messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name)

class SignUpView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('core:student_home')
        return render(request, self.template_name)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:landing')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class SubscriptionView(LoginRequiredMixin, FormView):
    template_name = 'accounts/subscription.html'
    form_class = SubscriptionForm
    success_url = reverse_lazy('core:student_home')
    
    def form_valid(self, form):
        profile = self.request.user.profile
        duration = form.cleaned_data['duration']
        
        if duration == '1_month':
            end_date = timezone.now() + relativedelta(months=1)
        elif duration == '6_months':
            end_date = timezone.now() + relativedelta(months=6)
        elif duration == '1_year':
            end_date = timezone.now() + relativedelta(years=1)
        
        profile.is_subscribed = True
        profile.subscription_end_date = end_date
        profile.save()
        
        return super().form_valid(form)