from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'root',
            'email': 'root@example.com',
            'password': '1234'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = reverse('token_obtain_pair')
        self.register_url = reverse('user-register')

    def test_user_registration(self):
        """测试用户注册"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """测试用户登录"""
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_detail(self):
        """测试获取用户详情"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
