from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.


class User(AbstractUser):
    def save(self, *args, **kwargs):
        created = not self.pk
        res = super().save(*args, **kwargs)
        if created:
            Cart.objects.create(user=self)
        return res


class Product(models.Model):
    title = models.CharField(max_length=50, db_index=True, unique=True)
    description = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    creatorId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="cart")

    @property
    def totalCost(self):
        sum = 0
        for item in self.items.all():
            sum += item.quantity * item.product.price
        return sum
    
    def __str__(self):
        return f"{self.user}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.product} ({self.quantity})"
    
    