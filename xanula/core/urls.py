from django.urls import path
from .views import AuthorLoginView, DownloadSolutionView, ExplanationRequestDetailView, ExplanationRequestView, NotificationListView, PastExamPaperDetailView, PastExamPaperListView, QuizAttempt, QuizResultView, QuizView, LandingPageView, StudentHomeView, WorkbookListView, WorkbookDetailView, AuthorDashboardView, get_explanation, workbook_analytics


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
    path('past-exam-papers/', PastExamPaperListView.as_view(), name='past_exam_paper_list'),
    path('past-exam-papers/<int:pk>/', PastExamPaperDetailView.as_view(), name='past_exam_paper_detail'),
    path('explanation-request/<int:question_id>/', ExplanationRequestView.as_view(), name='explanation_request'),
    path('explanation-request-detail/<int:pk>/', ExplanationRequestDetailView.as_view(), name='explanation_request_detail'),
    path('download-solution/<int:question_id>/', DownloadSolutionView.as_view(), name='download_solution'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
]



