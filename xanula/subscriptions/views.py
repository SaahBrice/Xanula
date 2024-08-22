from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Subscription, SubscriptionPlan

class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'subscriptions/subscription_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user).order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_subscription'] = Subscription.objects.filter(
            user=self.request.user,
            is_active=True,
            end_date__gt=timezone.now()
        ).first()
        return context

class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    template_name = 'subscriptions/subscription_create.html'
    fields = ['plan']
    success_url = reverse_lazy('subscriptions:subscription_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SubscriptionPlanListView(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'subscriptions/subscription_plan_list.html'
    context_object_name = 'plans'

class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    model = Subscription
    template_name = 'subscriptions/subscription_detail.html'
    context_object_name = 'subscription'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)