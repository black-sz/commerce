from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    购物车项序列化器
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """
    购物车序列化器
    """
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
        read_only_fields = ['user', 'created_at']


class AddToCartSerializer(serializers.Serializer):
    """
    添加到购物车序列化器
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
