from decimal import Decimal
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

# class PriceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prices
#         fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    price = serializers.SerializerMethodField()  
    currency = serializers.SerializerMethodField()

    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
           
            "price",
            "currency",
            
            "views",
            "rating",
            "category",
            "brand",
           
            "product_rating",
            "rating_count",
            "slug",
            "orders",
        ]

    def get_price(self, obj):
        currency_code = self.context.get('currency_code')
        if currency_code == 'EGP':
            return obj.price_EGP
        elif currency_code == 'AED':
            return obj.price_AED
        else:
            return None
        
    def get_currency(self, obj):
        currency_code = self.context.get('currency_code')
        if currency_code == 'EGP':
            return 'EGP'
        elif currency_code == 'AED':
            return 'AED'
        else:
            return None    

class ProductDetailSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True)
    color = ColorSerializer(many=True)
    size = SizeSerializer(many=True)
    specification = SpecificationSerializer(many=True)
    vendor =serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    price = serializers.SerializerMethodField()  
    currency = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "description",
            "category",
            "brand",
            #"price_EGP",
            #"price_AED",
            #"prices",
            "price",
            "currency",
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
    def get_price(self, obj):
        currency_code = self.context.get('currency_code')
        if currency_code == 'EGP':
            return obj.price_EGP
        elif currency_code == 'AED':
            return obj.price_AED
        else:
            return None
        
    def get_currency(self, obj):
        currency_code = self.context.get('currency_code')
        if currency_code == 'EGP':
            return 'EGP'
        elif currency_code == 'AED':
            return 'AED'
        else:
            return None     
    
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = representation.pop('product')
        currency_code = self.context.get('currency_code')

        # Check if converted_price exists in the product representation
        if 'price' in product_representation:
            representation['price'] = product_representation['price']

        if currency_code == 'EGP':
            price = product_representation.get('price_EGP')
        elif currency_code == 'AED':
            price = product_representation.get('price_AED')
        else:
            price = None

        # Set converted_price to price based on currency code
        product_representation['price'] = Decimal(price)
        product_representation['currency'] = currency_code

        # Remove price_EGP and price_AED fields
        product_representation.pop('price_EGP', None)
        product_representation.pop('price_AED', None)

        representation['product'] = product_representation
        return representation        

    


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





################################











class SummarySerializer(serializers.Serializer):
    products = serializers.IntegerField()
    orders = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)


class EarningSerializer(serializers.Serializer):
    monthly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)    
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)    



class CouponSummarySerializer(serializers.Serializer):
    total_coupons = serializers.IntegerField(default=0)
    active_coupons = serializers.IntegerField(default=0)    



class NotificationSummarySerializer(serializers.Serializer):
    un_read_noti = serializers.IntegerField(default=0)
    read_noti = serializers.IntegerField(default=0)
    all_noti = serializers.IntegerField(default=0)    




class ProductSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True,required=False)
    color = ColorSerializer(many=True,required=False)
    size = SizeSerializer(many=True,required=False)
    specification = SpecificationSerializer(many=True,required=False)
    #prices = PriceSerializer(many=True,required=False)
    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "description",
            "category",
            "price_EGP",
            "price_AED",
            #"prices",
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
            "orders",
        ]
    
    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3



class ProductAddSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True,required=False,read_only=True)
    color = ColorSerializer(many=True,required=False)
    size = SizeSerializer(many=True,required=False)
    specification = SpecificationSerializer(many=True,required=False)
    #prices = PriceSerializer(many=True,required=False)
    #image = serializers.SerializerMethodField()

    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "description",
            "category",
            "brand",
            "price_EGP",
            "price_AED",
            #"prices",
            "old_price",
            "shipping_amount",
            "stock_qty",
            "in_stock",
            "status",
            "featured",
            "views",
            #"rating",
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
            "orders",
        ]



    # def get_image(self, instance):
    #     request = self.context.get('request')
    #     if instance.image:
    #         return request.build_absolute_uri(instance.image.url)
    #     return None    
    
    def __init__(self, *args, **kwargs):
        super(ProductAddSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3            

