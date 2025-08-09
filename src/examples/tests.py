from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from src._test.models import Product, ProductCategory


class SearchProductTest(APITestCase):
    """
    An example how to use tests for any drf endpoints.
    
    For local running use: 
    
    >>> python manage.py test _test

    P.S. If you perform it on a Windows machine and encounter the error related to path 
    set this in opened terminal:

    >>> $env:PYTHONPATH="src"  

    OR for local docker

    >>> docker compose -f docker-compose.dev.yml exec gunicorn python manage.py test _test
    """
    def setUp(self):
        category = ProductCategory.objects.create(name="Electronics")
        Product.objects.create(name="iPhone", category=category)
        Product.objects.create(name="Samsung TV", category=category)
        Product.objects.create(name="Vacuum Cleaner", category=category)

        category = ProductCategory.objects.create(name="phones")
        Product.objects.create(name="Motorolla", category=category)

    def test_search_product_success(self):
        url = reverse('product-search')  # Name from urls.py
        response = self.client.get(url, {'q': 'Phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)

        products = response.data['result']
        
        self.assertEqual(len(products), 2)
        self.assertTrue(any('iPhone' in i['name'] for i in products))

    def test_search_product_no_query(self):
        url = reverse('product-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
