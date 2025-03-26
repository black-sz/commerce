from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from carts.models import CartItem
from products.models import Product
from django.db import transaction


class OrderListView(generics.ListAPIView):
    """
    订单列表视图
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    """
    订单详情视图
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrderView(APIView):
    """
    创建订单视图
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateOrderSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_items = serializer.validated_data['cart_items']
        cart_items = CartItem.objects.filter(id__in=cart_items, cart=request.user.cart)

        if not cart_items.exists():
            return Response({'error': '购物车中没有可购买的商品'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        order_items = []

        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response({'error': f'商品 {item.product.name} 库存不足'}, status=status.HTTP_400_BAD_REQUEST)

            total_amount += item.product.price * item.quantity
            order_items.append(OrderItem(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            ))

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount
        )

        for item in order_items:
            item.order = order
            item.save()
            product = item.product
            product.stock -= item.quantity
            product.save()

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
