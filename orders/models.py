from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Order(models.Model):
    """
    订单模型
    """
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="用户")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"订单 #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """
    订单项模型
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")

    class Meta:
        verbose_name = "订单项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.product.name} - 数量: {self.quantity}"
