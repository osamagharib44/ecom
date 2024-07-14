from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    """
    Custom user model

    Methods:
    - save: Override the save method to create an associated Cart instance
      whenever a new User is created.
    """

    def save(self, *args, **kwargs):
        created = not self.pk
        res = super().save(*args, **kwargs)
        if created:
            Cart.objects.create(user=self)
        return res


class Product(models.Model):
    """
    Model representing a product.

    Fields:
    - title: The title of the product (max length 50, unique, indexed).
    - description: A brief description of the product (max length 250, optional).
    - price: The price of the product (decimal with max digits 10 and 2 decimal places).
    - stock: The number of items available in stock (default 10, must be non-negative).
    - creatorId: The user who created the product (foreign key to User model).
    - createdAt: The date and time when the product was created (auto set).
    - updatedAt: The date and time when the product was last updated (auto set).
    """

    title = models.CharField(max_length=50, db_index=True, unique=True)
    description = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    creatorId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdProducts")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Cart(models.Model):
    """
    Model representing a shopping cart.

    Fields:
    - user: The user associated with the cart (one-to-one relationship with User model).
    - totalCost: The total cost of the items in the cart (read-only property).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="cart")

    @property
    def totalCost(self):
        """
        Calculates the total cost of all items in the cart.
        """
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
    
    