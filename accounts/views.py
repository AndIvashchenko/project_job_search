from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from .forms import RegistrationForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class MySignupView(CreateView):
    form_class = RegistrationForm
    success_url = 'login'
    template_name = 'register.html'
