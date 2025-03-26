from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {
            'name': '洗发水',
            'description': '去屑',
            'price': '10.99',
            'stock': 100
        }
        self.product = Product.objects.create(**self.product_data)
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})

    def test_get_products(self):
        response = self.client.get(self.list_url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        response = self.client.post(self.list_url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product(self):
        update_data = {'price': '15.99'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.price, 15.99)

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
