from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)  # Optional if needed
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    card_rate = models.DecimalField(max_digits=10, decimal_places=2)
    replacement_rate = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
    
class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.location}"
