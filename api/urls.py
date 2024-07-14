from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views_products, views_auth, views_cart

urlpatterns = [
    # Authentication endpoints
    path("auth", TokenObtainPairView.as_view(), name="auth"),
    path("auth/register", views_auth.AuthRegisterView.as_view(), name="auth-register"),
    
    # User endpoints
    path("users", views_auth.UserView.as_view(), name="users-all"),
    path("users/<int:id>", views_auth.UserView.as_view(), name="users-single"),
    
    # Product endpoints
    path("products", views_products.ProductView.as_view(), name="products-all"),
    path("products/<int:id>", views_products.ProductView.as_view(), name="products-single"),
    
    # Cart endpoints
    path("cart", views_cart.CartView.as_view(), name="cart-list"),
    path("cart/<int:productId>", views_cart.CartView.as_view(), name="cart-update"),
    path("cart/checkout", views_cart.CartCheckoutView.as_view(), name="cart-checkout"),
]
