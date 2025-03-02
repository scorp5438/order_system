import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger_console = logging.getLogger('console_logger')
logger_file = logging.getLogger('file_logger')


@shared_task
def order_creation(order):
    """
    Асинхронная задача для обработки создания заказа.

    Args:
        order (dict): Данные заказа, включая ID,
        email клиента и название товара.
    """
    order_pk = order.get('id')
    customer_email = order.get('customer_email')

    logger_console.debug(f'Заказ № {order_pk} создан')
    logger_file.debug(f'Заказ № {order_pk} создан')

    context = {
        'pk': order_pk,
        'product': order.get('product_name'),
    }

    html_message = render_to_string('email/create_order.html', context)

    email = EmailMessage(
        f'Заказ № {order_pk} оформлен',
        html_message,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
    )

    email.content_subtype = "html"
    email.send()


@shared_task
def order_update_status(order):
    """
    Асинхронная задача для обработки обновления статуса заказа.

    Args:
        order (dict): Данные заказа, включая ID, email клиента и новый статус.
    """
    order_pk = order.get('id')
    customer_email = order.get('customer_email')
    status = order.get('status')
    logger_console.debug(f'У заказ № {order_pk} изменен статус на {status}')
    logger_file.debug(f'У заказ № {order_pk} изменен статус на {status}')

    context = {
        'pk': order_pk,
        'status': status,
    }

    html_message = render_to_string('email/update_order.html', context)

    email = EmailMessage(
        f'Статус заказа с номером № {order_pk} успешно обновлен.',
        html_message,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
    )

    email.content_subtype = "html"
    email.send()


@shared_task
def order_creation_invalid_data(error_message):
    """
    Асинхронная задача для логирования ошибок при создании заказа.

    Args:
        error_message (dict): Данные заказа.
    """
    logger_console.error(f'Ошибка при создании заказа: {error_message}')
    logger_file.error(f'Ошибка при создании заказа: {error_message}')


@shared_task
def order_update_invalid_data(error_message):
    """
    Асинхронная задача для логирования ошибок при изменении статуса заказа.

    Args:
        error_message (dict): Данные заказа.
    """
    logger_console.error(f'Ошибка при обновлении заказа: {error_message}')
    logger_file.error(f'Ошибка при обновлении заказа: {error_message}')
