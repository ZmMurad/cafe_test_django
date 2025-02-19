from django.test import TestCase
from django.urls import reverse
from .models import Order, Item, OrderItem


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        """
        Инициализация тестовых данных.
        """
        self.item = Item.objects.create(item_name="Pizza", item_price=10.5)
        self.order = Order.objects.create(table_number=1, status='pending')

    def test_order_creation(self) -> None:
        """
        Проверяем, что заказ корректно создаётся.
        """
        self.assertEqual(self.order.table_number, 1)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.order_items.count(), 0)

    def test_order_item_addition(self) -> None:
        """
        Проверяем, что можно добавить позицию (OrderItem) в заказ.
        """
        OrderItem.objects.create(order=self.order, item=self.item, quantity=2)
        self.assertEqual(self.order.order_items.count(), 1)
        self.assertEqual(self.order.total_price, 21)

    def test_list_orders_view(self) -> None:
        """
        Проверяем, что страница списка заказов доступна.
        """
        url = reverse('orders:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список заказов")
