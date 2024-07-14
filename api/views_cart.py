from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import Product,  Cart, CartItem
from .serializers import  CartSerializer


class CartGenericView(generics.GenericAPIView):
    """
    A generic view for handling cart-related operations, which will be extended for multiple views.
    Only authenticated users are allowed
    """
    serializer_class = CartSerializer
    lookup_field = "productId"

    # Only authenticated users are allowed
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self):
        """
        Retrieve the cart of the current authenticated user.
        """
        return Cart.objects.get(user=self.request.user)
    
    def get_cartItems(self):
        """
        Retrieve all items in the current user's cart.
        """
        return self.get_cart().items.all()

    def get_cartItem(self, productId, createIfNotExists=True):
        """
        Retrieve a specific cart item based on the product ID. If the item does not exist
        and createIfNotExists is True, a new cart item will be created.

        Args:
            productId (int): The ID of the product to retrieve from the cart.
            createIfNotExists (bool): Whether to create a new cart item if it does not exist (default is True).

        Returns:
            CartItem: The cart item associated with the specified product.
                      If createIfNotExists is False and the item does not exist, None is returned.
        """
        productToAdd = get_object_or_404(Product, pk=productId)
        matchedItemsList = self.get_cartItems().filter(product=productToAdd)

        if len(matchedItemsList) == 0:
            if createIfNotExists:
                item = CartItem.objects.create(
                    product=productToAdd, cart=self.get_cart(), quantity=0)
                return item
            else:
                return None
        else:
            return matchedItemsList[0]


class CartView(CartGenericView):
    """
    View for handling operations on the user's cart including retrieval, 
    adding items, updating quantities, and removing items.
    """

    # CRUD operations
    def get(self, request, *args, **kwargs):
        instance = self.get_cart()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Add a product to the cart. If the product already exists in the cart,
        increment its quantity by 1.
        """
        productId = kwargs.get(self.lookup_field)
        if productId is None:
            data = {"error": "No product ID provided"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        cart = self.get_cart()
        cartItem = self.get_cartItem(productId=productId)
        cartItem.quantity += 1

        cartItem.save()
        cart.save()
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update the quantity of a product in the cart.
        """
        productId = kwargs.get(self.lookup_field)
        if productId is None:
            data = {"error": "No product ID provided"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        quantity = request.data.get("quantity")
        if quantity is None or quantity <= 0:
            data = {"error": "Product quantity must EXIST and be GREATER than 0"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        cart = self.get_cart()
        cartItem = self.get_cartItem(productId=productId)
        cartItem.quantity = quantity

        cartItem.save()
        cart.save()
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Remove a product from the cart.
        """
        productId = kwargs.get(self.lookup_field)
        if productId is None:
            data = {"error": "No product ID provided"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        cart = self.get_cart()
        cartItem = self.get_cartItem(productId=productId)
        if cartItem:
            cartItem.delete()
            cart.save()

        return self.get(request, *args, **kwargs)


class CartCheckoutView(CartGenericView):
    """
    View for handling the checkout process of the user's cart.
    """

    def post(self, request, *args, **kwargs):
        """
        Checkout the user's cart. Ensure that the quantity ordered for each 
        product does not exceed the available stock.
        """
        cart = self.get_cart()
        for item in self.get_cartItems():
            if item.quantity > item.product.stock:
                data = {
                    "error": "Quantity ordered for some products exceeds their available stock."
                }
                return Response(data, status=status.HTTP_409_CONFLICT)

        for item in self.get_cartItems():
            item.product.stock -= item.quantity
            item.product.save()
            item.delete()

        cart.save()

        return Response({
            "message": "Cart checkout successful"
        }, status=status.HTTP_200_OK)
