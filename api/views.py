from rest_framework import generics, mixins, status, authentication, permissions
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


class ProductView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creatorId=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creatorId=self.request.user)

    def get(self, request, *args, **kwargs):
        lookup_pk = kwargs.get(self.lookup_field)
        if (lookup_pk):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        lookup_pk = kwargs.get(self.lookup_field)
        if (lookup_pk):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AuthRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer