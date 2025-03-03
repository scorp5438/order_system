from rest_framework import serializers

from orders.models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Orders.

    Используется для сериализации и десериализации всех полей модели Orders.
    """

    class Meta:
        """
        Мета-класс для определения модели и полей сериализатора.

        Attributes:
            model (Orders): Модель, с которой работает сериализатор.
            fields (str): Поля модели, которые будут сериализованы.
                          Используется '__all__' для включения всех полей.
        """
        model = Orders
        fields = '__all__'


class CreateOrderSerializer(OrdersSerializer):
    """
    Сериализатор для создания заказа.

    Наследует OrdersSerializer, но ограничивает поля, которые можно указать
    при создании заказа. Используется для валидации и создания новых заказов.
    """

    class Meta(OrdersSerializer.Meta):
        """
        Мета-класс для определения полей, доступных при создании заказа.

        Attributes:
            fields (tuple): Поля, которые можно указать при создании заказа.
            Включает 'product_name', 'quantity', 'customer_email'.
        """
        fields = 'product_name', 'quantity', 'customer_email'


class UpdateOrderSerializer(OrdersSerializer):
    """
    Сериализатор для обновления заказа.

    Наследует OrdersSerializer, но ограничивает поля, которые можно обновить.
    Используется для изменения статуса заказа.
    """

    class Meta(OrdersSerializer.Meta):
        """
        Мета-класс для определения полей, доступных при обновлении заказа.

        Attributes:
            fields (tuple): Поля, которые можно обновить.
            Включает только 'status'.
        """
        fields = 'status',
