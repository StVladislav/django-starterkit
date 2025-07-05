from django.db.models.signals import post_delete
from django.dispatch import receiver

from src._test.models import ProductImage


@receiver(post_delete, sender=ProductImage)
def delete_image_files(sender, instance, **kwargs):
    """Delete image file from the attached to a product"""
    if instance.image:
        instance.image.delete(save=False)
