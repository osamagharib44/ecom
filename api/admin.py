from django.contrib import admin
from .models import User, Product, Cart, CartItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'stock', 'creatorId', 'createdAt', 'updatedAt')
    search_fields = ('title', 'description')
    list_filter = ('createdAt', 'updatedAt', 'creatorId')
    date_hierarchy = 'createdAt'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'totalCost', 'items')
    search_fields = ('user__username',)
    
    
    def items(self, obj):
        return ", ".join([str(k) for k in obj.items.all()])

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__title')