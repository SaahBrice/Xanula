from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    
    # Workbook URLs
    path('workbooks/', views.WorkbookListView.as_view(), name='workbook_list'),
    path('workbooks/create/', views.WorkbookCreateView.as_view(), name='workbook_create'),
    path('workbooks/<int:pk>/update/', views.WorkbookUpdateView.as_view(), name='workbook_update'),
    path('workbooks/<int:pk>/delete/', views.WorkbookDeleteView.as_view(), name='workbook_delete'),
    
    # Subject URLs
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/update/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    
    # PastExamPaper URLs
    path('exam-papers/', views.PastExamPaperListView.as_view(), name='past_exam_paper_list'),
    path('exam-papers/create/', views.PastExamPaperCreateView.as_view(), name='past_exam_paper_create'),
    path('exam-papers/<int:pk>/update/', views.PastExamPaperUpdateView.as_view(), name='past_exam_paper_update'),
    path('exam-papers/<int:pk>/delete/', views.PastExamPaperDeleteView.as_view(), name='past_exam_paper_delete'),
    
    # Subscription URLs
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('subscriptions/create/', views.SubscriptionCreateView.as_view(), name='subscription_create'),
    path('subscriptions/<int:pk>/update/', views.SubscriptionUpdateView.as_view(), name='subscription_update'),
    path('subscriptions/<int:pk>/delete/', views.SubscriptionDeleteView.as_view(), name='subscription_delete'),
    
    # SubscriptionPlan URLs
    path('subscription-plans/', views.SubscriptionPlanListView.as_view(), name='subscription_plan_list'),
    path('subscription-plans/create/', views.SubscriptionPlanCreateView.as_view(), name='subscription_plan_create'),
    path('subscription-plans/<int:pk>/update/', views.SubscriptionPlanUpdateView.as_view(), name='subscription_plan_update'),
    path('subscription-plans/<int:pk>/delete/', views.SubscriptionPlanDeleteView.as_view(), name='subscription_plan_delete'),
    
    # User URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]