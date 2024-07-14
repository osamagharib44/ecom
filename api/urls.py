from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views_products, views_auth, views_cart

urlpatterns = [
    # Authentication endpoints
    path("auth", TokenObtainPairView.as_view(), name="auth"),
    
    # User endpoints
    path("users", views_auth.UserListCreate.as_view(), name="users-list-create"),
    path("users/<int:id>", views_auth.UserRetrieveUpdateDestroy.as_view(), name="users-single"),
    
    # Product endpoints
    path("products", views_products.ProductListCreate.as_view(), name="products-list-create"),
    path("products/<int:id>", views_products.ProductRetreieveUpdateDestroy.as_view(), name="products-single"),
    
    # Cart endpoints
    path("cart", views_cart.CartRetrieve.as_view(), name="cart-list"),
    path("cart/<int:productId>", views_cart.CartUpdate.as_view(), name="cart-update"),
    path("cart/checkout", views_cart.CartCheckout.as_view(), name="cart-checkout"),
]
