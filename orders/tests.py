from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User
from carts.models import Cart, CartItem


class OrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test3', 'test3@example.com', '1234')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='可乐', description='无糖', price='7.00', stock=200)
        self.cart = Cart.objects.get(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.create_order_url = reverse('create-order')
        self.order_list_url = reverse('order-list')

    def test_create_order(self):
        """测试创建订单"""
        data = {'cart_items': [self.cart_item.id]}
        response = self.client.post(self.create_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        """测试获取订单列表"""
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
