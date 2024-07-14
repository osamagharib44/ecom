from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path("auth", TokenObtainPairView.as_view(), name="auth"),
    path("auth/register", views.AuthRegisterView.as_view(), name="auth-register"),
    path("products", views.ProductView.as_view(), name="products-all"),
    path("products/<int:id>", views.ProductView.as_view(), name="products-single"),
    path("users", views.UserView.as_view(), name="users-all"),
    path("users/<int:id>", views.UserView.as_view(), name="users-single"),

]
