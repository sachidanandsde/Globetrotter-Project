from django.urls import path
from .views import get_random_destination, check_answer, create_user, get_leaderboard,get_user_score,challenge_friend

urlpatterns = [
    path('random-destination', get_random_destination, name='random-destination'),
    path('check-answer', check_answer, name='check-answer'),
    path('create-user', create_user, name='create-user'),
    path('leaderboard', get_leaderboard, name='leaderboard'),
    path('user-score', get_user_score, name='user-score'),
    path('challenge-friend', challenge_friend, name='challenge-friend'),
]
