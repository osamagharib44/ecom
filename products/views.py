from rest_framework import generics, mixins, status
from .models import Product
from .serializers import ProductSerializer

class ProductGetView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
    def get(self, request, *args, **kwargs):
        lookup_pk = kwargs.get(self.lookup_field)
        if (lookup_pk):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
        