import django_filters
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Orders
from .serializers import (OrdersSerializer,
                          CreateOrderSerializer,
                          UpdateOrderSerializer)
from .tasks import (order_creation,
                    order_update_status,
                    order_creation_invalid_data,
                    order_update_invalid_data)
from ..filtrers import OrderFilter


class OrdersApiView(ModelViewSet):
    """
    API ViewSet для управления заказами.

    Поддерживает следующие методы:
    - GET: Получение списка заказов или деталей конкретного заказа.
    - POST: Создание нового заказа.
    - PATCH: Обновление статуса заказа.

    Атрибуты:
    - queryset: QuerySet для получения всех заказов или одного заказа по id.
    - http_method_name: ['GET', 'POST', 'PATCH'].
    """
    queryset = Orders.objects.all().order_by('pk')
    http_method_name = ['GET', 'POST', 'PATCH']
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от HTTP-метода.

        Returns:
            Serializer: Класс сериализатора для текущего запроса.
        """
        if self.request.method == 'GET':
            return OrdersSerializer
        elif self.request.method == 'POST':
            return CreateOrderSerializer
        return UpdateOrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Создает новый заказ.

        Args:
            request (Request): Объект запроса.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ с данными созданного заказа или ошибками валидации.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            full_serializer = OrdersSerializer(instance)
            order_creation.delay(full_serializer.data)
            return Response(full_serializer.data, status.HTTP_201_CREATED)
        else:
            order_creation_invalid_data.delay(serializer.errors)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        update_serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        if update_serializer.is_valid():
            update_serializer.save()
            full_serializer = OrdersSerializer(instance)
            order_update_status.delay(full_serializer.data)
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        order_update_invalid_data.delay(update_serializer.errors)
        return Response(
            update_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
