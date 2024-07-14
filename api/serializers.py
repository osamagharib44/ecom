from rest_framework import serializers
from .models import Product, User, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    
    creatorId = serializers.ReadOnlyField(source='creatorId.id', required=False)
    class Meta:
        model = Product
        fields = "__all__"
        

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    
    password = serializers.CharField(write_only=True, required=False)
    createdProducts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'createdProducts')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    """
    
    items = serializers.StringRelatedField(many=True, read_only=True)
    totalCost = serializers.SerializerMethodField("getTotalCost")
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ("id", "user")
        
    def getTotalCost(self, *args, **kwargs):
        return self.instance.totalCost
        
class OptionalSerializer(serializers.BaseSerializer):
    pass
    
class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart Item.
    """
    
    class Meta:
        model = CartItem
        fields = ["quantity"]
        
        