from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=50,
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('created_at'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ['id']

    def __str__(self):
        return self.name
