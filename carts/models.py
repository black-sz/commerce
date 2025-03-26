from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    """
    购物车模型
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carts', verbose_name="用户")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"购物车 - {self.user.username}"


class CartItem(models.Model):
    """
    购物车项模型
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="购物车")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name = "购物车项"
        verbose_name_plural = verbose_name
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} - 数量: {self.quantity}"
