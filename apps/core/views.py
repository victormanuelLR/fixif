from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.edit import FormView
from apps.core.scrap import suap_login
import requests


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    redirect_field_name = 'next'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
    
        self.pre_login(request)
        if request.user.is_authenticated and self.redirect_authenticated_user:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def pre_login(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            suap_data = suap_login(username, password)
            print(suap_data)


        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        redirect_to = (
            self.request.POST.get(self.redirect_field_name)
            or self.request.GET.get(self.redirect_field_name)
        )
        if redirect_to and url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure()
        ):
            return redirect_to
        # fallback: settings.LOGIN_REDIRECT_URL 
        return resolve_url(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('redirect_field_name', self.redirect_field_name)
        context.setdefault(
            'redirect_field_value',
            self.request.POST.get(self.redirect_field_name, self.request.GET.get(self.redirect_field_name, ''))
        )
        return context
