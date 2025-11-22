from django.urls import path
from .views import (
    CustomerListCreateView,
    CustomerDetailView
)

urlpatterns = [
    # List all customers & create new customer
    path('customer/', CustomerListCreateView.as_view(), name='customer-list-create'),

    # Retrieve, update, delete a single customer
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
]
