from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='home'),  # Root URL shows new landing page
    path('receive_sms/', views.receive_sms, name='receive_sms'),
    path('test_sms/', views.test_sms_offline, name='test_sms_offline'),  # Test without SMS
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('dashboard/', views.my_dashboard, name='my_dashboard'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
]