from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly


class ProductView(generics.GenericAPIView, 
                  mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.CreateModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin):
    """
    View for manipulation of products.

    - Allows anyone to view products.
    - Allows users to create/edit/delete THEIR OWN products ONLY.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        """
        Ensure the product is created on behalf of the current user.
        """
        serializer.save(creatorId=self.request.user)

    # Basic CRUD operations
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests. List ALL products if no id is provided, 
        retrieve a product if id is provided.
        """
        lookup_pk = kwargs.get(self.lookup_field)
        if lookup_pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


