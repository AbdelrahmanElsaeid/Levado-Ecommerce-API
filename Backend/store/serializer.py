from rest_framework import serializers

from userauths.serializer import ProfileReviewSerializer, ProfileSerializer
from .models import Product,Category,Brand,Gallery,Specification,Color,Size,Cart,CartOrder,CartOrderItem,Coupon,ProductFaq,Review,Wishlist,Notification
from vendor.models import Vendor


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'        

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id','title','content']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    # gallery = GallerySerializer(many=True)
    # color = ColorSerializer(many=True)
    # size = SizeSerializer(many=True)
    # specification = SpecificationSerializer(many=True)
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            
            "price",
            
            "views",
            "rating",
            "category",
            "brand",
           
            "product_rating",
            "rating_count",
            "slug",
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True)
    color = ColorSerializer(many=True)
    size = SizeSerializer(many=True)
    specification = SpecificationSerializer(many=True)
    vendor =serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "description",
            "category",
            "brand",
            "price",
            "old_price",
            "shipping_amount",
            "stock_qty",
            "in_stock",
            "status",
            "featured",
            "views",
            "rating",
            "vendor",
            "pid",
            "slug",
            "date",
            "gallery",
            "specification",
            "size",
            "color",
            "product_rating",
            "rating_count",
        ]
    
    def __init__(self, *args, **kwargs):
        super(ProductDetailSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3



class ProductFaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFaq
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductFaqSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CartSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Cart
        fields = '__all__'
    
    # def __init__(self, *args, **kwargs):
    #     super(CartSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST':
    #         self.Meta.depth = 0
    #     else:
    #         self.Meta.depth = 3

class CartOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartOrderItem
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(CartOrderItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CartOrderSerializer(serializers.ModelSerializer):
    orderitem = CartOrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = CartOrder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

from django.conf import settings

class ReviewSerializer(serializers.ModelSerializer):
    
    
    profile = ProfileReviewSerializer()

   
    class Meta:
        model = Review
        fields = ['id','profile','review','rating','date']

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Wishlist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class WishlistListSerializer(serializers.ModelSerializer):
    # product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Wishlist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WishlistListSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3



class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CouponSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3




class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3








class ReviewSummarySerializer(serializers.Serializer):

    one_star = serializers.IntegerField(default=0)
    two_star = serializers.IntegerField(default=0)
    three_star = serializers.IntegerField(default=0)
    four_star = serializers.IntegerField(default=0)
    five_star = serializers.IntegerField(default=0)
