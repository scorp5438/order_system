import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrdersSerializer, CreateOrderSerializer, UpdateOrderSerializer
from orders.models import Orders
from .tasks import order_creation, order_update_status, order_creation_invalid_data, order_update_invalid_data


class OrdersApiView(ModelViewSet):
    queryset = Orders.objects.all()
    http_method_name = ['GET', 'POST', 'PATCH']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrdersSerializer
        elif self.request.method == 'POST':
            return CreateOrderSerializer
        return UpdateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.save()
            full_serializer = OrdersSerializer(instance)
            order_creation.delay(full_serializer.data.get('id'))
            return Response(full_serializer.data, status.HTTP_201_CREATED)
        else:
            order_creation_invalid_data.delay(serializer.errors)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if update_serializer.is_valid():
            update_serializer.save()
            full_serializer = OrdersSerializer(instance)
            order_update_status.delay(full_serializer.data.get('id'), request.data.get('status'))
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        order_update_invalid_data.delay(update_serializer.errors)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
