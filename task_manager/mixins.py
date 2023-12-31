from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class UserAuthenticateMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not authorized! Please sign in.'),
            )
            return redirect(reverse_lazy('login'))

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


class CheckTaskAuthorPermissionMixin(CheckUserPermissionMixin):
    """Verify task author permissions."""
    def test_func(self):
        return self.get_object().author == self.request.user


class DeleteRestrictionMixin:
    """Verify object is not used by other objects."""

    rejection_message = ''
    rejection_next_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.rejection_message)
            return redirect(self.rejection_next_url)
