from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductStockListCreateView,
    ProductStockRetrieveUpdateDestroyView,
)

app_name = 'inventory'

urlpatterns = [
    # Product APIs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

    # Product Stock APIs
    path('product-stock/', ProductStockListCreateView.as_view(), name='product-stock-list-create'),
    path('product-stock/<int:pk>/', ProductStockRetrieveUpdateDestroyView.as_view(), name='product-stock-detail'),
]
