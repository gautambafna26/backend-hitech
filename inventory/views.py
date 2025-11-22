from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Product,ProductStock
from .serializers import ProductSerializer,ProductStockSerializer
# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

# Product Stock Views
class ProductStockListCreateView(generics.ListCreateAPIView):
    queryset = ProductStock.objects.select_related('product').all().order_by('id')
    serializer_class = ProductStockSerializer
    permission_classes = [IsAuthenticated]

class ProductStockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductStock.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = [IsAuthenticated]