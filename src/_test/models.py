from django.db import models
from django.contrib.postgres.indexes import GinIndex

from utils.mixins import CreatedAtMixin
from utils.fields import ResizedImageField
from utils.functions import slugify


class ProductCategory(CreatedAtMixin):
    """
    For using GinIndex PostgresSQL it should be installed in a database server:
    CREATE EXTENSION IF NOT EXISTS pg_trgm

    It is example of how to use GinIndex for full-text search
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_category"
        managed = True
        indexes = [
            GinIndex(
                name="trgm_category_name_idx",
                fields=['name'],
                opclasses=['gin_trgm_ops']
            )
        ]


class Product(CreatedAtMixin):
    """
    For using GinIndex PostgresSQL it should be installed in a database server:
    CREATE EXTENSION IF NOT EXISTS pg_trgm

    It is example of how to use GinIndex for a full-text search and
    using resized image field with deleting image-file after deleting record.

    For deleting image-file need to set up pre-delete receivers in the receivers.py
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, Product, "slug")
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.slug}"

    class Meta:
        db_table = 'products'
        managed = True
        indexes = [
            GinIndex(
                name="trgm_product_search_idx",
                fields = ['name', 'slug',],
                opclasses=['gin_trgm_ops', 'gin_trgm_ops',]
            )
        ]


class ProductImage(CreatedAtMixin):
    image = ResizedImageField(
        upload_to="images",
        blank=True,
        null=True,
        verbose_name='Product image'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Is image main?",
    )

    def __str__(self):
        return f"{self.product.slug}"
