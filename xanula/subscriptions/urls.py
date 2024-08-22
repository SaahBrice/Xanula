from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('create/', views.SubscriptionCreateView.as_view(), name='subscription_create'),
    path('plans/', views.SubscriptionPlanListView.as_view(), name='subscription_plan_list'),
    path('<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription_detail'),
]