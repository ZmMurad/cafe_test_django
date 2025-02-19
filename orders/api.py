from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'created_at', 'total_price', 'order_items']


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций над заказами.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        """
        Пример эндпоинта для поиска заказов по номеру стола или статусу.
        """
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()
        if query:
            queryset = queryset.filter(table_number__icontains=query) | queryset.filter(status__icontains=query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
