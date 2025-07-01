from rest_framework import serializers
from src._test.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    class Meta:
        model = Product
        fields = ("id", "name", "category", "slug", "image")
