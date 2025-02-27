import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrdersSerializer, CreateOrderSerializer, UpdateOrderSerializer
from orders.models import Orders

logger = logging.getLogger('console_logger')
logger_2 = logging.getLogger('file_logger')

class OrdersApiView(ModelViewSet):
    queryset = Orders.objects.all()
    http_method_name = ['GET', 'POST', 'PATCH']
    methods = {
        'GET': OrdersSerializer,
        'PATCH': UpdateOrderSerializer,
        'PUT': UpdateOrderSerializer,
        'POST': CreateOrderSerializer
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrdersSerializer
        elif self.request.method == 'POST':
            return CreateOrderSerializer
        return UpdateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer =  self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.save()
            full_serializer = OrdersSerializer(instance)
            logger.debug(f'Заказ № {full_serializer.data.get('id')} создан')
            return Response(full_serializer.data, status.HTTP_201_CREATED)
        else:
            logger.error(f'Ошибка при создании заказа: {serializer.errors}')
            logger_2.error(f'Ошибка при создании заказа: {serializer.errors}')
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if update_serializer.is_valid():
            update_serializer.save()
            full_serializer = OrdersSerializer(instance)
            logger.debug(f'Заказ № {full_serializer.data.get('id')} обновлен')
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        logger.error(f'Ошибка при создании заказа: {update_serializer.errors}')
        logger_2.error(f'Ошибка при создании заказа: {update_serializer.errors}')
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)