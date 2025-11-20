from django.urls import path
from .views import (
    ProductListCreateView,
)

app_name = 'inventory'

urlpatterns = [
    # Product APIs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
