from datetime import datetime
from django.db import models


class CreatedAtMixin(models.Model):
    """
    Use this insted of default django models.Model. 
    This class add automatically add created_at and updated_at fields
    to a model. After each save updated_at field will be update
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Created'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Updated'
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
