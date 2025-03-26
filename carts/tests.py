from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from carts.models import Cart, CartItem
from products.models import Product
from users.models import User


class CartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test4', 'test4@example.com', '1234')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='面包', description='酸奶面包', price='4.12', stock=60)
        self.cart = Cart.objects.get(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.add_to_cart_url = reverse('add-to-cart')
        self.update_cart_item_url = reverse('update-cart-item', kwargs={'pk': self.cart_item.pk})
        self.remove_from_cart_url = reverse('remove-from-cart', kwargs={'pk': self.cart_item.pk})

    def test_add_to_cart(self):
        """测试添加商品到购物车"""
        data = {'product_id': self.product.id, 'quantity': 1}
        response = self.client.post(self.add_to_cart_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cart_item(self):
        """测试更新购物车项"""
        data = {'quantity': 3}
        response = self.client.patch(self.update_cart_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_cart(self):
        """测试从购物车中移除商品"""
        response = self.client.delete(self.remove_from_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
