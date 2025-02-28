from celery import shared_task
import logging

logger_console = logging.getLogger('console_logger')
logger_file = logging.getLogger('file_logger')


@shared_task
def order_creation(order_id: int):
    logger_console.debug(f'Заказ № {order_id} создан')
    logger_file.debug(f'Заказ № {order_id} создан')


@shared_task
def order_update_status(order_id: int, new_status: str):
    logger_console.debug(f'У заказ № {order_id} изменен статус на {new_status}')
    logger_file.debug(f'У заказ № {order_id} изменен статус на {new_status}')


@shared_task
def order_creation_invalid_data(error_message):
    logger_console.error(f'Ошибка при создании заказа: {error_message}')
    logger_file.error(f'Ошибка при создании заказа: {error_message}')


@shared_task
def order_update_invalid_data(error_message):
    logger_console.error(f'Ошибка при обновлении заказа: {error_message}')
    logger_file.error(f'Ошибка при обновлении заказа: {error_message}')
