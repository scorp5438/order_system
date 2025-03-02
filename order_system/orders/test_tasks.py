import logging
from unittest import TestCase
from unittest.mock import patch

from orders.api.tasks import (order_creation,
                              order_update_status,
                              order_creation_invalid_data,
                              order_update_invalid_data)


class CeleryTasksTestCase(TestCase):
    def test_order_creation(self):
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
        error_message = 'Invalid data'

        with patch.object(
                logging.getLogger('console_logger'),
                'error'
        ) as mock_logger:
            order_update_invalid_data(error_message)
            mock_logger.assert_called_with(
                'Ошибка при обновлении заказа: Invalid data'
            )
