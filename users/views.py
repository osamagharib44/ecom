from rest_framework import generics, mixins, status
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    
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
    
        