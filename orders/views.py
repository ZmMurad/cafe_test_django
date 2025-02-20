from typing import Union, Optional
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Sum, F
from django.views.generic import ListView

from .models import Order, OrderItem, Item
from .forms import OrderCreateForm, OrderItemForm, ItemCreateForm, OrderItemFormSet


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        status_filter = self.request.GET.get('status')

        if search_query:
            queryset = queryset.filter(table_number=search_query)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.Status.choices
        return context





def order_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Отображает детали конкретного заказа (Order),
    включая связанные OrderItem.

    :param request: HttpRequest
    :param pk: первичный ключ заказа
    :return: HttpResponse с деталями заказа
    """
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order,
        'items': order.order_items.all(),
    }
    return render(request, 'orders/order_detail.html', context)


def order_create(request):
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        order_item_formset = OrderItemFormSet(request.POST)

        new_item_names = request.POST.getlist('new_item_name[]')
        new_item_prices = request.POST.getlist('new_item_price[]')
        new_item_quantities = request.POST.getlist('new_item_quantity[]')

        if order_form.is_valid():
            order = order_form.save()

            if order_item_formset.is_valid():
                order_items = order_item_formset.save(commit=False)
                for order_item in order_items:
                    order_item.order = order
                    order_item.save()

            for name, price, quantity in zip(new_item_names, new_item_prices, new_item_quantities):
                if name and price:
                    new_item = Item.objects.create(item_name=name, item_price=price)
                    OrderItem.objects.create(order=order, item=new_item, quantity=quantity)

            return redirect('orders:order_detail', pk=order.pk)

    else:
        order_form = OrderCreateForm()
        order_item_formset = OrderItemFormSet()

    context = {
        'order_form': order_form,
        'order_item_formset': order_item_formset,
    }
    return render(request, 'orders/order_create.html', context)


def order_edit(request, pk):
    """
    Редактирует существующий заказ: позволяет добавлять, удалять и изменять блюда в заказе.
    """
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST, instance=order)
        order_item_formset = OrderItemFormSet(request.POST, instance=order)
        item_form = ItemCreateForm(request.POST)

        if order_form.is_valid():
            order_form.save()
            if order_item_formset.is_valid():
                order_item_formset.save()
            new_item_name = request.POST.get('item_name')
            new_item_price = request.POST.get('item_price')
            if new_item_name and new_item_price:
                new_item = Item.objects.create(item_name=new_item_name, item_price=new_item_price)
                quantity = request.POST.get('new_item_quantity', 1)
                OrderItem.objects.create(order=order, item=new_item, quantity=quantity)

            if order.pk:
                return redirect('orders:order_detail', pk=order.pk)
            else:
                return redirect('orders:order_list')


    else:
        order_form = OrderCreateForm(instance=order)
        order_item_formset = OrderItemFormSet(instance=order)
        item_form = ItemCreateForm()

    context = {
        'order_form': order_form,
        'order_item_formset': order_item_formset,
        'item_form': item_form,
    }
    return render(request, 'orders/order_edit.html', context)


def order_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Удаляет заказ по pk.

    :param request: HttpRequest
    :param pk: первичный ключ заказа
    :return: Редирект на список заказов
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:order_list')
    context = {'order': order}
    return render(request, 'orders/order_delete.html', context)


def calculate_revenue(request: HttpRequest) -> HttpResponse:
    """
    Подсчитывает суммарную выручку по всем заказам со статусом 'оплачено'.

    :param request: HttpRequest
    :return: HttpResponse с суммарной выручкой
    """
    paid_orders = OrderItem.objects.filter(order__status='paid')
    revenue = paid_orders.aggregate(
        total=Sum(F('item__item_price') * F('quantity'))
    )['total'] or 0

    return render(request, 'orders/revenue.html', {'revenue': revenue})
