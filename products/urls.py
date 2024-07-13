from django.urls import path
from . import views

urlpatterns = [
    path("products",views.ProductGetView.as_view() ,name="products-list"),
    path("products/<int:pk>",views.ProductGetView.as_view() ,name="products-retrieve"),
    path("products",views.ProductGetView.as_view() ,name="products-create"),
    path("products/<int:pk>",views.ProductGetView.as_view() ,name="products-update"),
]
