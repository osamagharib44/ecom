from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly


class AuthRegisterView(generics.CreateAPIView):
    """
        View to allow users to register their account by using Create API View
    """
    serializer_class = UserSerializer


class UserView(generics.GenericAPIView, 
               mixins.ListModelMixin, 
               mixins.RetrieveModelMixin, 
               mixins.UpdateModelMixin, 
               mixins.DestroyModelMixin):
    """
    View for manipulation of users.

    - Allows anyone to read user information.
    - Only admins can edit or delete users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly
    ]

    # Basic CRUD operations
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests. List ALL users if no id is provided, 
        retrieve a user if id is provided.
        """
        lookup_pk = kwargs.get(self.lookup_field)
        if lookup_pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
 

