from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50, db_index=True, unique=True)
    description = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
