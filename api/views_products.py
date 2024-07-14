from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly


class ProductListCreate(generics.ListCreateAPIView, 
                  mixins.ListModelMixin):
    """
    View for listing and create products

    - Allows anyone to list products.
    - Only authenticated users can create products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Ensure the product is created on behalf of the current user.
        """
        serializer.save(creatorId=self.request.user)


class ProductRetreieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    View for manipulation of products.

    - Allows users to create/edit/delete THEIR OWN products ONLY.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]


