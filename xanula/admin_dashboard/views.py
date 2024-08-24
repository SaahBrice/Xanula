from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from core.models import Chapter, ExplanationRequest, Notification, Quiz, Workbook, Subject, PastExamPaper
from subscriptions.models import Subscription, SubscriptionPlan
from django.contrib import messages
from .forms import ExplanationResponseForm, NotificationForm, PastExamPaperForm, SubjectForm, SubscriptionForm, SubscriptionPlanForm, UserForm, WorkbookForm

User = get_user_model()

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'admin_dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['total_workbooks'] = Workbook.objects.count()
        context['total_subscriptions'] = Subscription.objects.count()
        context['total_exam_papers'] = PastExamPaper.objects.count()
        return context

# Workbook views
class WorkbookListView(StaffRequiredMixin, ListView):
    model = Workbook
    template_name = 'admin_dashboard/workbook_list.html'
    context_object_name = 'workbooks'
    paginate_by = 20

class WorkbookCreateView(StaffRequiredMixin, CreateView):
    model = Workbook
    form_class = WorkbookForm
    template_name = 'admin_dashboard/workbook_form.html'
    success_url = reverse_lazy('admin_dashboard:workbook_list')

    def form_valid(self, form):
        messages.success(self.request, 'Workbook created successfully.')
        return super().form_valid(form)

class WorkbookUpdateView(StaffRequiredMixin, UpdateView):
    model = Workbook
    form_class = WorkbookForm
    template_name = 'admin_dashboard/workbook_form.html'
    success_url = reverse_lazy('admin_dashboard:workbook_list')

    def form_valid(self, form):
        messages.success(self.request, 'Workbook updated successfully.')
        return super().form_valid(form)

class WorkbookDeleteView(StaffRequiredMixin, DeleteView):
    model = Workbook
    template_name = 'admin_dashboard/workbook_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:workbook_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Workbook deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Subject views
class SubjectListView(StaffRequiredMixin, ListView):
    model = Subject
    template_name = 'admin_dashboard/subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 20

class SubjectCreateView(StaffRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'admin_dashboard/subject_form.html'
    success_url = reverse_lazy('admin_dashboard:subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject created successfully.')
        return super().form_valid(form)

class SubjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'admin_dashboard/subject_form.html'
    success_url = reverse_lazy('admin_dashboard:subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject updated successfully.')
        return super().form_valid(form)

class SubjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Subject
    template_name = 'admin_dashboard/subject_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:subject_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subject deleted successfully.')
        return super().delete(request, *args, **kwargs)

# PastExamPaper views
class PastExamPaperListView(StaffRequiredMixin, ListView):
    model = PastExamPaper
    template_name = 'admin_dashboard/past_exam_paper_list.html'
    context_object_name = 'exam_papers'
    paginate_by = 20

class PastExamPaperCreateView(StaffRequiredMixin, CreateView):
    model = PastExamPaper
    form_class = PastExamPaperForm
    template_name = 'admin_dashboard/past_exam_paper_form.html'
    success_url = reverse_lazy('admin_dashboard:past_exam_paper_list')

    def form_valid(self, form):
        messages.success(self.request, 'Past Exam Paper created successfully.')
        return super().form_valid(form)

class PastExamPaperUpdateView(StaffRequiredMixin, UpdateView):
    model = PastExamPaper
    form_class = PastExamPaperForm
    template_name = 'admin_dashboard/past_exam_paper_form.html'
    success_url = reverse_lazy('admin_dashboard:past_exam_paper_list')

    def form_valid(self, form):
        messages.success(self.request, 'Past Exam Paper updated successfully.')
        return super().form_valid(form)

class PastExamPaperDeleteView(StaffRequiredMixin, DeleteView):
    model = PastExamPaper
    template_name = 'admin_dashboard/past_exam_paper_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:past_exam_paper_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Past Exam Paper deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Subscription views
class SubscriptionListView(StaffRequiredMixin, ListView):
    model = Subscription
    template_name = 'admin_dashboard/subscription_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 20

class SubscriptionCreateView(StaffRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'admin_dashboard/subscription_form.html'
    success_url = reverse_lazy('admin_dashboard:subscription_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subscription created successfully.')
        return super().form_valid(form)

class SubscriptionUpdateView(StaffRequiredMixin, UpdateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'admin_dashboard/subscription_form.html'
    success_url = reverse_lazy('admin_dashboard:subscription_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subscription updated successfully.')
        return super().form_valid(form)

class SubscriptionDeleteView(StaffRequiredMixin, DeleteView):
    model = Subscription
    template_name = 'admin_dashboard/subscription_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:subscription_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subscription deleted successfully.')
        return super().delete(request, *args, **kwargs)

# SubscriptionPlan views
class SubscriptionPlanListView(StaffRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'admin_dashboard/subscription_plan_list.html'
    context_object_name = 'subscription_plans'
    paginate_by = 20

class SubscriptionPlanCreateView(StaffRequiredMixin, CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'admin_dashboard/subscription_plan_form.html'
    success_url = reverse_lazy('admin_dashboard:subscription_plan_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subscription Plan created successfully.')
        return super().form_valid(form)

class SubscriptionPlanUpdateView(StaffRequiredMixin, UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'admin_dashboard/subscription_plan_form.html'
    success_url = reverse_lazy('admin_dashboard:subscription_plan_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subscription Plan updated successfully.')
        return super().form_valid(form)

class SubscriptionPlanDeleteView(StaffRequiredMixin, DeleteView):
    model = SubscriptionPlan
    template_name = 'admin_dashboard/subscription_plan_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:subscription_plan_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subscription Plan deleted successfully.')
        return super().delete(request, *args, **kwargs)

# User views
class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'admin_dashboard/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    template_name = 'admin_dashboard/user_form.html'
    fields = ['username', 'email', 'password', 'is_staff', 'is_active']
    success_url = reverse_lazy('admin_dashboard:user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'admin_dashboard/user_form.html'
    success_url = reverse_lazy('admin_dashboard:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)

class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = User
    template_name = 'admin_dashboard/user_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ExplanationRequestListView(StaffRequiredMixin, ListView):
    model = ExplanationRequest
    template_name = 'admin_dashboard/explanation_request_list.html'
    context_object_name = 'explanation_requests'
    paginate_by = 20

    def get_queryset(self):
        return ExplanationRequest.objects.all().order_by('-created_at')

class ExplanationRequestResponseView(StaffRequiredMixin, UpdateView):
    model = ExplanationRequest
    form_class = ExplanationResponseForm
    template_name = 'admin_dashboard/explanation_request_response.html'
    success_url = reverse_lazy('admin_dashboard:explanation_request_list')

    def form_valid(self, form):
        form.instance.responded_at = timezone.now()
        return super().form_valid(form)
    

class NotificationCreateView(StaffRequiredMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'admin_dashboard/notification_create.html'
    success_url = reverse_lazy('admin_dashboard:notification_list')

    def form_valid(self, form):
        if form.cleaned_data['send_to_all']:
            form.instance.is_global = True
            form.instance.recipient = None
        messages.success(self.request, 'Notification sent successfully.')
        return super().form_valid(form)

class NotificationListView(StaffRequiredMixin, ListView):
    model = Notification
    template_name = 'admin_dashboard/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

