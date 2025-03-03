import django_filters

from .models import Orders


class OrderFilter(django_filters.FilterSet):
    """
    Фильтр для модели Orders.

    Позволяет фильтровать заказы по следующим полям:
    - status: Точное совпадение статуса заказа.
    - product_name: Частичное совпадение названия товара (без учета регистра).
    - customer_email: Частичное совпадение email клиента (без учета регистра).
    """

    class Meta:
        """
        Мета-класс для настройки фильтра.

        Атрибуты:
        - model: Модель, к которой применяется фильтр (Orders).
        - fields: Поля модели, по которым можно фильтровать, и типы фильтрации.
        """
        model = Orders
        fields = {
            'status': ['exact'],
            'product_name': ['icontains'],
            'customer_email': ['icontains'],
        }
