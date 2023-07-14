from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Label
from task_manager.mixins import UserAuthenticateMixin, DeleteRestrictionMixin


class LabelListView(UserAuthenticateMixin, ListView):
    """View for list all labels from database."""
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/main.html'


class LabelCreateView(UserAuthenticateMixin, SuccessMessageMixin, CreateView):
    """View for form to create a new label."""
    model = Label
    fields = ['name']
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')


class LabelUpdateView(UserAuthenticateMixin, SuccessMessageMixin, UpdateView):
    """View to update existing status information."""
    model = Label
    fields = ('name',)
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully updated')


class LabelDeleteView(UserAuthenticateMixin, SuccessMessageMixin,
                      DeleteRestrictionMixin, DeleteView):
    """View to delete existing user."""
    model = Label
    template_name = 'labels/delete.html'
    success_message = _('Label successfully deleted')
    success_url = reverse_lazy('labels')
    rejection_message = _("Unable to delete label because it's in use")
    rejection_next_url = reverse_lazy('labels')
