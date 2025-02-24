from rest_framework import serializers

from orders.models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class CreateOrderSerializer(OrdersSerializer):
    class Meta(OrdersSerializer.Meta):
        fields = 'product_name', 'quantity', 'customer_email'


class UpdateOrderSerializer(OrdersSerializer):
    class Meta(OrdersSerializer.Meta):
        fields = 'status',
