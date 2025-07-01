from django.db.models.signals import pre_delete
from django.dispatch import receiver

from src._test.models import Product


@receiver(pre_delete, sender=Product)
def delete_image_files(sender, instance, **kwargs):
    """Delete image file from the attached to a product"""
    if instance.image:
        instance.image.delete(save=False)
