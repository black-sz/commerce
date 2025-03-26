from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    用户模型
    """
    email = models.EmailField(unique=True, verbose_name="邮箱")
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    # 添加 related_name 参数
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name="分组",
        help_text="指定用户所属的组。"
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name="用户权限",
        help_text="指定用户具有的具体权限。"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
