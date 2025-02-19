from typing import Any

from django.db import models

# Create your models here.
class Item(models.Model):
    """
    Модель блюда (позиции меню).
    """
    item_name: str = models.CharField(max_length=100)
    item_price: float = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        """
        Возвращает строковое представление блюда.
        """
        return self.item_name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'В ожидании'
        READY = 'ready', 'Готово'
        PAID = 'paid', 'Оплачено'
    """
    Модель заказа в кафе.
    """
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    )

    table_number: int = models.PositiveIntegerField()
    status: str = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at: Any = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self) -> float:
        """
        Рассчитывает суммарную стоимость заказа
        на основе связанных позиций (OrderItem).
        """
        items = self.order_items.all()
        return sum([oi.item.item_price * oi.quantity for oi in items])

    def __str__(self) -> str:
        """
        Возвращает строковое представление заказа.
        """
        return f"Order #{self.pk} (Table {self.table_number})"


class OrderItem(models.Model):
    """
    Связующая модель между заказом и блюдами.
    Содержит информацию о том, сколько раз блюдо встречается в заказе.
    """
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item: Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity: int = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """
        Возвращает краткую информацию о позиции в заказе.
        """
        return f"{self.item.item_name} x {self.quantity}"