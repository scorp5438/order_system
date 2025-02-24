from django.db.models import Count
from django.test import TestCase
from django.urls import reverse

from .models import Orders


class OrdersApiViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.order_1 = Orders.objects.create(
            product_name='Laptop',
            quantity=2,
            customer_email='132@gmail.com'
        )
        cls.order_2 = Orders.objects.create(
            product_name='Phone',
            quantity=5,
            customer_email='777@yandex.ru'
        )

    @classmethod
    def tearDownClass(cls):
        Orders.objects.all().delete()

    def setUp(self):
        self.data = {
            'product_name': 'Book',
            'quantity': 5,
            'customer_email': 'example@yandex.ru'
        }

    def test_get_all_orders(self):
        response = self.client.get(reverse('orders:orders-list'))
        response_data = response.json()
        status_order_1 = response_data[0].get('status')
        email = response_data[1].get('customer_email')

        self.assertEqual(len(response_data), 2)
        self.assertEqual(status_order_1, 'created')
        self.assertEqual(email, '777@yandex.ru')

    def test_get_one_order(self):
        current_order_pk = self.order_2.pk
        response = self.client.get(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}))
        response_data = response.json()

        self.assertEqual(response_data.get('id'), current_order_pk)
        self.assertEqual(response_data.get('product_name'), self.order_2.product_name)
        self.assertEqual(response_data.get('customer_email'), self.order_2.customer_email)
        self.assertEqual(response_data.get('status'), self.order_2.status)

    def test_get_one_order_non_existent_pk(self):
        current_order_pk = Orders.objects.all().aggregate(Count('pk')).get('pk__count') + 1
        response = self.client.get(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}))
        response_data = response.json()
        status_code = response.status_code
        expected_response = 'No Orders matches the given query.'

        self.assertEqual(status_code, 404)
        self.assertEqual(response_data.get('detail'), expected_response)


    def test_create_order_valid_data(self):
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()

        self.assertEqual(response_data.get('product_name'), self.data.get('product_name'))
        self.assertEqual(response_data.get('quantity'), self.data.get('quantity'))
        self.assertEqual(response_data.get('customer_email'), self.data.get('customer_email'))

    def test_create_order_invalid_product_name(self):
        self.data['product_name'] = ''

        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        expected_response = 'This field may not be blank.'
        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('product_name'))

    def test_create_order_invalid_quantity(self):
        self.data['quantity'] = 0

        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        expected_response = 'The quantity must be greater than zero.'
        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('quantity'))

    def test_create_order_invalid_quantity_below_zero(self):
        self.data['quantity'] = -1

        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        expected_response = 'The quantity must be greater than zero.'
        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('quantity'))


    def test_create_order_invalid_quantity_not_int(self):
        self.data['quantity'] = ''

        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        expected_response = 'A valid integer is required.'
        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('quantity'))

    def test_create_order_invalid_email(self):
        self.data['customer_email'] = '1234@mail'

        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        expected_response = 'Enter a valid email address.'
        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('customer_email'))


    def test_create_order_email_is_blank(self):
        self.data['customer_email'] = ''

        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        expected_response = 'This field may not be blank.'
        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('customer_email'))

    def test_update_order(self):
        self.data = {
            'status': 'processing'
        }
        current_order_pk = self.order_1.pk
        response = self.client.patch(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertEqual(response_data.get('status'), self.data.get('status'))
        self.assertEqual(response_data.get('id'), current_order_pk)
        self.assertEqual(response_data.get('product_name'), self.order_1.product_name)


    def test_update_order_invalid_data(self):
        self.data = {
            'status': 'test'
        }
        current_order_pk = self.order_1.pk
        response = self.client.patch(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}), data=self.data, content_type='application/json')
        response_data = response.json()
        status_code = response.status_code
        expected_response = 'is not a valid choice.'

        self.assertEqual(status_code, 400)
        self.assertIn(expected_response, response_data.get('status')[0])