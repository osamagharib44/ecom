from django.urls import path
from . import views

urlpatterns = [
    path("products", views.ProductView.as_view() ,name="products-all"),
    path("products/<int:pk>", views.ProductView.as_view() ,name="products-single"),

]
