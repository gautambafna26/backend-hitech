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