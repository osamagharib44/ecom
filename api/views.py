from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, authentication, permissions
from rest_framework.response import Response
from .models import Product, User, Cart, CartItem
from .serializers import ProductSerializer, UserSerializer, CartSerializer
from .permissions import IsOwnerOrReadOnly

class AuthRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

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


class CartGenericView(generics.GenericAPIView):
    serializer_class = CartSerializer
    lookup_field = "productId"

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(pk=self.request.user)
 
    
    def get_cart(self):
        return Cart.objects.get(pk=self.request.user)
 
    
    def get_cartItem(self, productId, createIfNotExists=True):
        productToAdd = get_object_or_404(Product, pk = productId)
        cart = self.get_cart()
        matchedItemsList = CartItem.objects.filter(product=productToAdd, cart=cart)
        
        if (len(matchedItemsList)==0):
            if (createIfNotExists):
                item = CartItem.objects.create(product=productToAdd, cart=cart, quantity=0)
                return item
            else:
                return None
        else:
            item = matchedItemsList[0]
            return item      


class CartView(CartGenericView):
    def get(self, request, *args, **kwargs):
        instance = self.get_cart()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
    def post(self, request, *args, **kwargs):
        productId = kwargs.get(self.lookup_field)
        if productId==None:
            data = {
                "error": "No product ID provided"
            }
            return Response(data ,status=status.HTTP_400_BAD_REQUEST)
        
        cart = self.get_cart()
        cartItem = self.get_cartItem(productId=productId)
        cartItem.quantity += 1
        
        cartItem.save()
        cart.save()
        return self.get(request, *args, **kwargs)

        
    def put(self, request, *args, **kwargs):        
        productId = kwargs.get(self.lookup_field)
        if productId==None:
            data = {
                "error": "No product ID provided"
            }
            return Response(data ,status=status.HTTP_400_BAD_REQUEST)
        
        quantity = request.data.get("quantity")        
        if (quantity==None or quantity<=0):
            data = {
                "error": "Product quantity must EXIST and be GREATER than 0"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)  
        
        cart = self.get_cart()
        cartItem = self.get_cartItem(productId=productId)
        cartItem.quantity = quantity
        
        cartItem.save()
        cart.save()
        return self.get(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        productId = kwargs.get(self.lookup_field)
        if productId==None:
            data = {
                "error": "No product ID provided"
            }
            return Response(data ,status=status.HTTP_400_BAD_REQUEST)
        
        cart = self.get_cart()
        cartItem = self.get_cartItem(productId=productId)
        if (cartItem):            
            cartItem.delete()
            cart.save()
            
        return self.get(request, *args, **kwargs)


class CartCheckoutView(CartGenericView):
    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        for item in cart.items:
            if (item.quantity>item.product.stock):
                data = {
                    "error": "Quantity ordered for some products exceeds their available stock in the market"
                }
                return Response(data ,status=status.HTTP_409_CONFLICT)
            
        for item in cart.items:
            item.delete()
            
        cart.totalCost = 0
        cart.save()
 