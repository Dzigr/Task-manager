from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from django.utils.translation import gettext_lazy as _

from .models import Task
from task_manager.apps.labels.models import Label


class TaskFilter(FilterSet):
    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label')
    )

    user_task = BooleanFilter(
        field_name='author',
        label=_('Only your tasks'),
        method='filter_tasks_by_user',
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filter_tasks_by_user(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user.pk)
        return queryset
