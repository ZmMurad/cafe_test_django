from django.contrib import admin
from .models import Order, Item, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'total_price', 'created_at')
    list_filter = ('status',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_price')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'quantity')
