from django.urls import path
from apps.webapp.views import IndexView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]