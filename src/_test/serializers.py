from rest_framework import serializers
from src._test.models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer contains get_images method for returning field images as
    a list or url and is_main keys. You can use this for handling
    foreign keys like this.

    P.S. If you want to create new products using category name not its ID - you will need to 
    re-write create and update methods.
    """
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = serializers.SerializerMethodField()
    

    def get_images(self, obj):
        request = self.context.get('request')
        out = []
        for image_obj in obj.images.all():
            if image_obj.image:
                url = image_obj.image.url
                if request:
                    url = request.build_absolute_uri(url)
                out.append({
                    "url": url,
                    "is_main": image_obj.is_main,
                })
        return out
    

    class Meta:
        model = Product
        fields = ("id", "name", "category", "category_name", "slug", "images")
        read_only_fields = ['slug', 'created_at']
