from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly

class UserListCreate(generics.ListCreateAPIView):
    """
    View for listing and creating of users.

    - Allows anyone to list all user information.
    - Allows anyone to create new accouns
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
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
