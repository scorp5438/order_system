from django.core.validators import validate_email
from django.db import models


class Orders(models.Model):
    statuses = [
        ('created', 'created'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    ]

    product_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Наименование товара')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество товара')
    customer_email = models.EmailField(max_length=255, validators=[validate_email], verbose_name='e-mail')
    status = models.CharField(max_length=15, default='created', choices=statuses, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'

    def __str__(self):
        return f'Order id: {self.pk}, product: {self.product_name}'
