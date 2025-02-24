from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrdersSerializer, CreateOrderSerializer, UpdateOrderSerializer
from orders.models import Orders

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if update_serializer.is_valid():
            update_serializer.save()
            full_serializer = OrdersSerializer(instance)
            return Response(full_serializer.data, status=status.HTTP_200_OK)

        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)