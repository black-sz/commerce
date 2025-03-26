from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    商品序列化器
    """
    class Meta:
        model = Product
        fields = '__all__'
