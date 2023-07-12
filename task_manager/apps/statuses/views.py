from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import StatusForm
from .models import Status
from task_manager.mixins import UserAuthenticateMixin


class StatusListView(UserAuthenticateMixin, ListView):
    """View for list all statuses from database."""
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/main.html'


class StatusCreateView(UserAuthenticateMixin, SuccessMessageMixin, CreateView):
    """View for form to create a new status."""
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')


class StatusUpdateView(UserAuthenticateMixin, SuccessMessageMixin, UpdateView):
    """View to update existing status information."""
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')


class StatusDeleteView(UserAuthenticateMixin, SuccessMessageMixin, DeleteView):
    """View to delete existing user."""
    model = Status
    template_name = 'statuses/delete.html'
    success_message = _('Status successfully deleted')
    success_url = reverse_lazy('statuses')
