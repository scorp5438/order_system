from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrdersApiView

router = DefaultRouter()
app_name = 'orders'
# Маршрут для отображения списка заказов
# 1/orders/{pk} отображение заказа по id
router.register('v1/orders', OrdersApiView, basename='orders')


urlpatterns = [
    path('', include(router.urls))
]
# urlpatterns += router.urls
