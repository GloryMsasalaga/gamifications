from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.leaderboard, name='home'),  # Root URL shows leaderboard
    path('receive_sms/', views.receive_sms, name='receive_sms'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
]