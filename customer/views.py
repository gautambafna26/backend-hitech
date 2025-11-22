from django.shortcuts import render
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated


# Get +post
class CustomerListCreateView(generics.ListCreateAPIView):
    """List all customers or create a new customer."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

# Get(single) + put + delete

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a customer."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]