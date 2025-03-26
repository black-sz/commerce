from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from products.models import Product
from django.shortcuts import get_object_or_404


class CartDetailView(generics.RetrieveAPIView):
    """
    购物车详情视图
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return self.request.user.cart


class AddToCartView(APIView):
    """
    添加商品到购物车视图
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = AddToCartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        product = get_object_or_404(Product, id=product_id)
        cart = request.user.cart

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': '商品已添加到购物车'}, status=status.HTTP_200_OK)


class UpdateCartItemView(generics.UpdateAPIView):
    """
    更新购物车项视图
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.quantity <= 0:
            instance.delete()


class RemoveFromCartView(generics.DestroyAPIView):
    """
    从购物车中移除商品视图
    """
    queryset = CartItem.objects.all()
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': '商品已从购物车中移除'}, status=status.HTTP_200_OK)
