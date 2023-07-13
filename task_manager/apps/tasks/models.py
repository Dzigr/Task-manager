from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.apps.statuses.models import Status
from task_manager.apps.labels.models import Label


class Task(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('author'),
    )

    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('executor'),
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('status'),
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        related_name='labels',
        verbose_name=_('labels'),
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    class TaskLabelRelation(models.Model):
        task = models.ForeignKey('Task', on_delete=models.CASCADE)
        label = models.ForeignKey(Label, on_delete=models.PROTECT)
