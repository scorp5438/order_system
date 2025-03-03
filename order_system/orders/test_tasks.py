import logging
from unittest import TestCase
from unittest.mock import patch

from orders.api.tasks import (order_creation,
                              order_update_status,
                              order_creation_invalid_data,
                              order_update_invalid_data)


class CeleryTasksTestCase(TestCase):
    """
    Тестовый класс для проверки Celery задач, связанных с заказами.

    Этот класс тестирует задачи Celery,
    такие, как создание заказа, обновление статуса заказа,
    а также обработку ошибок при невалидных данных.
    """

    def test_order_creation(self):
        """
        Тест задачи создания заказа.

        Проверяет, что при успешном создании заказа:
        1. Отправляется email-уведомление.
        2. Записывается лог с информацией о создании заказа.
        """
        order_data = {
            'id': 1,
            'product_name': 'Laptop',
            'customer_email': 'test@example.com',
        }

        with patch('django.core.mail.EmailMessage.send') as mock_send:
            with patch.object(
                    logging.getLogger('console_logger'),
                    'debug'
            ) as mock_logger:
                order_creation(order_data)
                mock_send.assert_called_once()
                mock_logger.assert_called_with('Заказ № 1 создан')

    def test_order_update_status(self):
        """
        Тест задачи обновления статуса заказа.

        Проверяет, что при успешном обновлении статуса заказа:
        1. Отправляется email-уведомление.
        2. Записывается лог с информацией об изменении статуса.
        """
        order_data = {
            'id': 1,
            'customer_email': 'test@example.com',
            'status': 'completed',
        }

        with patch('django.core.mail.EmailMessage.send') as mock_send:
            with patch.object(
                    logging.getLogger('console_logger'),
                    'debug'
            ) as mock_logger:
                order_update_status(order_data)
                mock_send.assert_called_once()
                mock_logger.assert_called_with(
                    'У заказ № 1 изменен статус на completed'
                )

    def test_order_creation_invalid_data(self):
        """
        Тест обработки ошибки при создании заказа с невалидными данными.

        Проверяет, что при возникновении ошибки:
        1. Записывается лог с сообщением об ошибке.
        """
        error_message = 'Invalid data'

        with patch.object(
                logging.getLogger('console_logger'),
                'error'
        ) as mock_logger:
            order_creation_invalid_data(error_message)
            mock_logger.assert_called_with(
                'Ошибка при создании заказа: Invalid data'
            )

    def test_order_update_invalid_data(self):
        """
        Тест обработки ошибки при обновлении заказа с невалидными данными.

        Проверяет, что при возникновении ошибки:
        1. Записывается лог с сообщением об ошибке.
        """
        error_message = 'Invalid data'

        with patch.object(
                logging.getLogger('console_logger'),
                'error'
        ) as mock_logger:
            order_update_invalid_data(error_message)
            mock_logger.assert_called_with(
                'Ошибка при обновлении заказа: Invalid data'
            )
