from django.db import models


class Product(models.Model):
    """
    商品模型
    """
    name = models.CharField(max_length=200, verbose_name="商品名称")
    description = models.TextField(verbose_name="商品描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(verbose_name="库存")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name
