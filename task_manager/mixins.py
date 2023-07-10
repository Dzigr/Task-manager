from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class UserAuthenticateMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.permission_denied_message = _('You are not authorized!'
                                               'Please sign in.')
            self.permission_forwarded_url = reverse_lazy('login')

        return super().dispatch(request, *args, **kwargs)


class CheckUserPermissionMixin(UserPassesTestMixin):
    """Verify user permissions."""
    permission_denied_message = ''
    permission_forwarded_url = ''

    def test_func(self):
        user = self.get_object()
        return user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_forwarded_url)
