from django.views.generic.base import TemplateView 
from apps.core.models import UserProfile
from django.shortcuts import redirect
from apps.core.models import Report

class IndexView(TemplateView):
    template_name = "webapp/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('webapp:feed')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeedView(TemplateView):
    template_name = "webapp/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        if user_profile:
            context['user_profile'] = user_profile

        
        context['reports'] = Report.objects.filter(
            is_active=True
        )

        return context

class ProfileView(TemplateView):
    template_name = "webapp/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        if user_profile:
            context['user_profile'] = user_profile

        return context
