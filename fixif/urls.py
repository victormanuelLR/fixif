
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, logout_then_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.webapp.urls', namespace='webapp')),
    path('accounts/login/', LoginView.as_view(redirect_authenticated_user=True), name='login')]

