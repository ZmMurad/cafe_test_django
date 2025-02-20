from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Item


class OrderCreateForm(forms.ModelForm):
    """Форма создания заказа"""

    class Meta:
        model = Order
        fields = ['table_number', 'status']


class ItemCreateForm(forms.ModelForm):
    """Форма для создания нового блюда"""
    item_name = forms.CharField(required=False, label="Название блюда")
    item_price = forms.DecimalField(required=False, label="Цена (руб)", min_value=0)

    class Meta:
        model = Item
        fields = ['item_name', 'item_price']


class OrderItemForm(forms.ModelForm):
    """Форма для добавления блюд в заказ"""

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']


OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)
