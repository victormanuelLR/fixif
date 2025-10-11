from django.urls import path
from apps.webapp.views import *

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('profile/', ProfileView.as_view(), name='profile'),
]