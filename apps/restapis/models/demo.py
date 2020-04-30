"""Demo Model"""
from django.db import models
from django.utils import timezone


class Demo(models.Model):
    """Demo Model."""

    message = models.TextField(max_length=50, default=0)
    created = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        """Meta Class."""

        db_table = 'demo'