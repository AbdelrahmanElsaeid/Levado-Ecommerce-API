from django.shortcuts import render
from store.models import Category,Product,Cart,Tax,CartOrder,CartOrderItem,Review,Brand
from store.serializer import CartSerializer, ProductListSerializer,ProductDetailSerializer,CategorySerializer,CartOrderSerializer,ReviewSerializer,BrandSerializer
from rest_framework import generics,status
from rest_framework.permissions import AllowAny 
from userauths.models import User
from decimal import Decimal
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .myfilter import ProductFilter
from .mypagination import ProductPagination
# Create your views here.
from django.db.models import Q


class Fpro(generics.ListAPIView):

    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all()
      

        brand_ids_str = self.request.query_params.get('brand_ids')
        category_ids_str = self.request.query_params.get('category_ids')
        prices_str = self.request.query_params.get('price')
        rating_str = self.request.query_params.get('rating')
        title_query = self.request.query_params.get('title')

        

        brand_ids = []
        category_ids = []
        prices = []
        min_price = None
        max_price = None
        rating = None

        if brand_ids_str:
            if brand_ids_str != '[]':
                brand_ids = [int(id) for id in brand_ids_str.strip('[]').split(',')]
        
        if category_ids_str:
            if category_ids_str != '[]':
                category_ids = [int(id) for id in category_ids_str.strip('[]').split(',')]

        if prices_str:
            if prices_str != '[]':
                prices = [float(price) for price in prices_str.strip('[]').split(',')]
                min_price, max_price = prices[0], prices[1] if len(prices) > 1 else None 

        # if rating_str:  
        #     if rating_str != '[]':  
        #         rating_values = [int(rating) for rating in rating_str.strip('[]').split(',')]
        #         rating = rating_values[0]

        if rating_str:  
            if rating_str != '':  
                rating = int(rating_str)
        

        #-------------------filter---------------

        #print(f"rating-------{rating}")


        if brand_ids:
            queryset = queryset.filter(brand__id__in=brand_ids)

        if category_ids:
            queryset = queryset.filter(category__id__in=category_ids)

        if min_price is not None and max_price is not None:
            queryset = queryset.filter(price__range=(min_price, max_price))

        if rating is not None:
            queryset = queryset.filter(rating__gte=rating)

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)                

        return queryset















class CategoryListAPIView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class= CategorySerializer
    permission_classes = [AllowAny]


class BrandListAPIView(generics.ListAPIView):
    queryset=Brand.objects.all()
    serializer_class= BrandSerializer
    permission_classes = [AllowAny] 


class ProductBrandListAPIView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class= ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        name=self.kwargs.get('brand')
        if name:
            brand= Brand.objects.get(title=name)
            queryset = Product.objects.filter(brand=brand)
        else: 
            queryset=Product.objects.all()    
        return queryset


class ProductCategory(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class= ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        name=self.kwargs.get('category')
        if name:
            category= Category.objects.get(title=name)
            queryset = Product.objects.filter(category=category)
        else: 
            queryset=Product.objects.all()    
        return queryset


class ProductListAPIView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class= ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    filterset_class = ProductFilter



class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class=ProductDetailSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        slug=self.kwargs['slug']
        query = Product.objects.get(slug=slug)
        return query  



class ReviewListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[AllowAny,]


    def get_queryset(self):
        product_id = self.kwargs['product_id']

        product=Product.objects.get(id=product_id)
        reviews=Review.objects.filter(product=product)
        return reviews
    
    def create(self,request,*args, **kwargs):
        payload = request.data

        user_id = payload['user_id']
        product_id= payload['product_id']
        rating = payload['rating']
        review = payload['review']

        user = User.objects.get(id=user_id)
        product=Product.objects.get(id=product_id)


        Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            review=review,
        )

        return Response({"message":"Review Created Successfully"}, status=status.HTTP_201_CREATED)
    



class CartAPIView(generics.ListCreateAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[AllowAny]  


    def create(self, request, *args, **kwargs):
        payload=request.data 

        product_id=payload['product_id']
        user_id=payload['user_id']
        qty=payload['qty']
        price=payload['price']
        shipping_amount=payload['shipping_amount']
        country=payload['country']
        size=payload['size']
        color=payload['color']
        cart_id=payload['cart_id']


        product=Product.objects.get(id=product_id)

        if user_id != "undefined":
            user = User.objects.get(id=user_id)

        else:
            user = None 

        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate /100
        else:
            tax_rate = 0

        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

        if cart:
            cart.user=user
            cart.product=product
            cart.qty=qty
            cart.price=price
            cart.sub_total= Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color=color
            cart.size=size
            cart.country=country
            cart.cart_id=cart_id


            service_fee_percentage = 10 / 100
            cart.service_fee = Decimal(service_fee_percentage)  * cart.sub_total

            cart.total =cart.sub_total + cart.shipping_amount + cart.tax_fee
            cart.save()
            return Response({'message': "Cart Updated Successfully"}, status=status.HTTP_200_OK)

        else:
            cart=Cart()
            cart.user=user
            cart.product=product
            cart.qty=qty
            cart.price=price
            cart.sub_total= Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color=color
            cart.size=size
            cart.country=country
            cart.cart_id=cart_id


            service_fee_percentage = 10 / 100
            cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

            cart.total =cart.sub_total + cart.shipping_amount + cart.tax_fee
            cart.save()
            return Response({'message': "Cart Created Successfully"}, status=status.HTTP_201_CREATED)



class CartListView(generics.ListAPIView):
    serializer_class=CartSerializer
    queryset= Cart.objects.all()
    permission_classes=[AllowAny,]


    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')


        if user_id is not None:
            user = User.objects.get(id=int(user_id))
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset    


class CartDetailView(generics.RetrieveAPIView):
    serializer_class=CartSerializer
    queryset= Cart.objects.all()
    permission_classes=[AllowAny,]


    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')


        if user_id is not None:
            user = User.objects.get(id=int(user_id))
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset  
    

    def get(self,*args, **kwargs):
        queryset=self.get_queryset()

        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_subtotal = 0.0
        total_total = 0.0


        for cart_item in queryset:
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_subtotal += float(self.calculate_subtotal(cart_item))
            total_total += float(self.calculate_total(cart_item))



        data = {
            'shipping': total_shipping,
            'tax': total_tax,
            'service_fee': total_service_fee,
            'sub_total': total_subtotal,
            'total': round(total_total,2),
        } 

        return Response(data)   



    def calculate_shipping(self,cart_item):
        return cart_item.shipping_amount
    def calculate_tax(self,cart_item):
        return cart_item.tax_fee
    def calculate_service_fee(self,cart_item):
        return cart_item.service_fee
    def calculate_subtotal(self,cart_item):
        return cart_item.sub_total
    def calculate_total(self,cart_item):
        return cart_item.total        


class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class=CartSerializer
    lookup_field='cart_id'

    def get_object(self, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        item_id = self.kwargs['item_id']
        cart_id = self.kwargs['cart_id']

        if user_id:
            user =User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id, user=user, cart_id=cart_id)
        else:
            cart = Cart.objects.get(id=item_id, cart_id=cart_id)    


        return cart
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    


class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer  
    queryset = CartOrder.objects.all()
    permission_classes= [AllowAny,]  


    def create(self, request, *args, **kwargs):
        payload = request.data


        fullname = payload['full_name']
        mobile = payload['mobile']
        address = payload['address']
        state = payload['state']
        city = payload['city']
        country = payload['country']
        email = payload['email']

        cart_id = payload['cart_id']
        user_id = payload['user_id']
        print(f"user id ======== {user_id}")

        if user_id == 0:
            
            user=None
        else:
            user=User.objects.get(id=user_id)

        print(f"user  ======== {user}")    
            

        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_shipping = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_service_fee = Decimal(0.00)
        total_subtotal = Decimal(0.00)
        total_total = Decimal(0.00)

        order = CartOrder.objects.create(

        buyer=user,
        full_name =fullname, 
        mobile =mobile,
        address = address, 
        state = state, 
        city = city, 
        country = country,  
        email = email, 

        )


        for c in cart_items:
            CartOrderItem.objects.create(
                order=order,
                product=c.product,
                vendor = c.product.vendor,
                qty=c.qty,
                price=c.price,
                sub_total= c.sub_total,
                shipping_amount = c.shipping_amount,
                tax_fee = c.tax_fee,
                color=c.color,
                size=c.size,
                country=c.country,
                total = c.total,
                initial_total =c.total,


            )

            total_shipping += Decimal(c.shipping_amount) 
            total_tax += Decimal(c.tax_fee) 
            total_service_fee += Decimal(c.service_fee) 
            total_subtotal += Decimal(c.sub_total) 
            total_total += Decimal(c.total)


            order.vendor.add(c.product.vendor)

        order.sub_total= total_subtotal
        order.shipping_amount = total_shipping
        order.tax_fee =total_tax
        order.service_fee = total_service_fee
        order.total=total_total
        order.initial_total=total_total

        order.save()

        return Response({"message": "Order created successfully", "order_oid":order.oid}, status=status.HTTP_201_CREATED)     


class CheckoutView(generics.RetrieveAPIView):
    serializer_class= CartOrderSerializer
    lookup_field ='order_oid'

    def get_object(self):
        order_oid = self.kwargs['order_oid']
        order = CartOrder.objects.get(oid=order_oid)
        return order