from django.urls import path
from . import views

urlpatterns = [
    path("products",views.ProductGetView,name="products-list")
]
