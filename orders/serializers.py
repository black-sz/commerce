from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    订单项序列化器
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """
    订单序列化器
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """
    创建订单序列化器
    """
    cart_items = serializers.ListField(child=serializers.IntegerField(), write_only=True)
