from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class IndexView(SuccessMessageMixin, TemplateView):
    template_name = 'index.html'
    success_message = 'sdada'


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'user_auth.html'
    next_page = reverse_lazy('main')
    success_message = _("You're logged in")


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('main')
    success_message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You're logged out"))
        return super().dispatch(request, *args, **kwargs)