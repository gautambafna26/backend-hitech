from rest_framework import serializers
from .models import Product, ProductStock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'unit_price',
            'card_rate', 'replacement_rate', 'weight',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProductStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = ProductStock
        fields = [
            'id', 'product', 'product_id', 'quantity',
            'location', 'last_restocked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']