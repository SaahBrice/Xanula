from django.urls import path
from .views import AuthorLoginView, QuizAttempt, QuizResultView, QuizView, LandingPageView, StudentHomeView, WorkbookListView, WorkbookDetailView, AuthorDashboardView, get_explanation, workbook_analytics


app_name = 'core'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('home/', StudentHomeView.as_view(), name='student_home'),
    path('subject/<int:subject_id>/', WorkbookListView.as_view(), name='workbook_list'),
    path('workbook/<int:pk>/', WorkbookDetailView.as_view(), name='workbook_detail'),
    path('author/dashboard/<str:unique_code>/', AuthorDashboardView.as_view(), name='author_dashboard'),
    path('quiz/<int:quiz_id>/', QuizView.as_view(), name='quiz'),
    path('quiz_result/<int:attempt_id>/', QuizResultView.as_view(), name='quiz_result'),
    path('get_explanation/', get_explanation, name='get_explanation'),
    path('author/login/', AuthorLoginView.as_view(), name='author_login'),
    path('workbook/<int:workbook_id>/analytics/', workbook_analytics, name='workbook_analytics'),
]



