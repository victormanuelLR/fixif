from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.edit import FormView
from django.contrib.auth import logout
from apps.core.models import Campus

from apps.core.models import UserProfile  
from apps.core.scrap import suap_login

User = get_user_model()

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    redirect_field_name = 'next'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.redirect_authenticated_user:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def pre_login(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return None

        suap_data = suap_login(username, password)
        if not suap_data.get("success"):
            return None

        details = suap_data["details"]

        profile = UserProfile.objects.filter(suap_username=username).first()

        if suap_data['account_type'] == 'student':
            campus = details['course'].split('-')[-2].strip()
            campus_obj, created = Campus.objects.get_or_create(campus_name=campus)
            if created:
                campus_obj.save()


            if profile:
                profile.suap_avatar_url = details["picture"]
                profile.suap_nickname = details["nickname"]
                profile.suap_full_name = details["name"]
                profile.suap_course = details["course"]
                profile.campus = campus_obj
                profile.save()
                user = profile.user
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=details["name"].split()[0],
                    last_name=" ".join(details["name"].split()[1:]),
                )
                UserProfile.objects.create(
                    user=user,
                    suap_username=username,
                    suap_avatar_url=details["picture"],
                    suap_nickname=details["nickname"],
                    suap_full_name=details["name"],
                    suap_course=details["course"],
                    campus=campus_obj

                )
        else:
            return None


        auth_login(request, user)
        return user

    def post(self, request, *args, **kwargs):
        user = self.pre_login(request)
        if user:
            return redirect(self.get_success_url())

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        redirect_to = (
            self.request.POST.get(self.redirect_field_name)
            or self.request.GET.get(self.redirect_field_name)
        )
        if redirect_to and url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return redirect_to
        return resolve_url(getattr(settings, "LOGIN_REDIRECT_URL", "/"))

class LogoutView(FormView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('webapp:index')