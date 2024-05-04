from django.shortcuts import render

# Create your views here.
from .models import Vendor
from store.serializer import SummarySerializer, ProductSerializer,CartOrderItemSerializer,CartOrderSerializer, EarningSerializer, ReviewSerializer,CouponSerializer,CouponSummarySerializer,NotificationSerializer,NotificationSummarySerializer,VendorSerializer, ColorSerializer,SpecificationSerializer,SizeSerializer,GallerySerializer,ProductAddSerializer,ColorAddSerializer,SizeAddSerializer,SpecificationAddSerializer,ProductListSerializer
from django.shortcuts import render,redirect
from store.models import Category,Product,Cart,Tax,CartOrder,CartOrderItem,Coupon,Notification,Review
from rest_framework import generics,status
from rest_framework.permissions import AllowAny 
from userauths.models import User,Profile
from userauths.serializer import ProfileSerializer
from django.db import transaction
from django.conf import settings
from decimal import Decimal
from rest_framework.response import Response
from django.db import models
import requests
from django.db.models.functions import ExtractMonth
from datetime import datetime, time, timedelta
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
# Create your views here.



class DashboardStatsAPIView(generics.ListAPIView):
    serializer_class = SummarySerializer
    permission_classes=[AllowAny,]

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)

        #calculate summary value

        product_count = Product.objects.filter(vendor=vendor).count()
        order_count = CartOrder.objects.filter(vendor=vendor, payment_status='paid').count()
        revenue = CartOrderItem.objects.filter(vendor=vendor, order__payment_status="paid").aggregate(total_revenue=models.Sum(models.F('sub_total') + models.F('shipping_amount')))['total_revenue'] or 0


        return [{
            'products': product_count,
            'orders':order_count,
            'revenue': revenue,
        }]
    

    def list(self,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)



@api_view(('GET',))
def MonthlyOrderChartAPIView(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    orders = CartOrder.objects.filter(vendor=vendor, payment_status='paid')
    orders_by_month = orders.annotate(month=ExtractMonth("date")).values("month").annotate(orders=models.Count("id")).order_by("month")
    return Response(orders_by_month)


@api_view(('GET',))
def MonthlyProductChartAPIView(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    products = Product.objects.filter(vendor=vendor)
    products_by_month = products.annotate(month=ExtractMonth("date")).values("month").annotate(products=models.Count("id")).order_by("month")
    return Response(products_by_month)



class ProductsAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer#ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        products = Product.objects.filter(vendor=vendor)
        return products
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['currency_code'] = self.kwargs.get('currency')
        return context 


class OrdersAPIView(generics.ListAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        orders = CartOrder.objects.filter(vendor=vendor, payment_status="paid")
        return orders
    
class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny,]

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        order_oid = self.kwargs['order_oid']
        vendor = Vendor.objects.get(id=vendor_id)
        
        return CartOrder.objects.get(vendor=vendor, oid=order_oid) 


class RevenueAPIView(generics.ListAPIView):
    serializer_class = CartOrderItemSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        revenue = CartOrderItem.objects.filter(vendor=vendor, order__payment_status="paid").aggregate(
            total_revenue=models.Sum(models.F('sub_total') + models.F('shipping_amount')))['total_revenue'] or 0
        return revenue
    



class FilterProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        filter = self.request.GET.get("filter")
        if filter == "published":
            products = Product.objects.filter(vendor=vendor, status="published")
        elif filter == "in_review":  
            products = Product.objects.filter(vendor=vendor, status="in_review")
        elif filter == "draft":  
            products = Product.objects.filter(vendor=vendor, status="draft")  
        elif filter == "disabled":  
            products = Product.objects.filter(vendor=vendor, status="disabled")
        else:
            products = Product.objects.filter(vendor=vendor)
        return products

class EarningAPIView(generics.ListAPIView):
    serializer_class= EarningSerializer
    permission_classes= [AllowAny,]  

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)

        one_month_ago = datetime.today() - timedelta(days=28)
        monthly_revenue = CartOrderItem.objects.filter(vendor=vendor, order__payment_status="paid", date__gte=one_month_ago).aggregate(total_revenue=models.Sum(models.F('sub_total') + models.F('shipping_amount')))['total_revenue'] or 0
        total_revenue = CartOrderItem.objects.filter(vendor=vendor, order__payment_status="paid").aggregate(total_revenue=models.Sum(models.F('sub_total') + models.F('shipping_amount')))['total_revenue'] or 0

        return[{
            'monthly_revenue':monthly_revenue,
            'total_revenue':total_revenue,
             
         }]
    
    def list(self,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    

@api_view(('GET',))
def MonthlyEarningTracker(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    monthly_earning_tracker = (
        CartOrderItem.objects
        .filter(vendor=vendor, order__payment_status="paid")
        .annotate(
            month=ExtractMonth("date")
        )
        .values("month")
        .annotate(
            sales_count=models.Sum("qty"),
            total_earning=models.Sum(
                models.F('sub_total') + models.F('shipping_amount'))
        )
        .order_by("-month")
    )
    return Response(monthly_earning_tracker)



class ReviewsListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        reviews = Review.objects.filter(product__vendor=vendor)
        return reviews



class ReviewsDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        review_id = self.kwargs['review_id']

        vendor = Vendor.objects.get(id=vendor_id)
        review = Review.objects.get(product__vendor=vendor, id=review_id)
        return review



class CouponListAPIView(generics.ListAPIView):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permission_classes = (AllowAny, )

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        coupon = Coupon.objects.filter(vendor=vendor)
        return coupon


class CouponCreateAPIView(generics.CreateAPIView):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        payload = request.data

        vendor_id = payload['vendor_id']
        code = payload['code']
        discount = payload['discount']
        active = payload['active']

        print("vendor_id ======", vendor_id)
        print("code ======", code)
        print("discount ======", discount)
        print("active ======", active)

        vendor = Vendor.objects.get(id=vendor_id)
        coupon = Coupon.objects.create(
            vendor=vendor,
            code=code,
            discount=discount,
            active=(active.lower() == "true")
        )

        return Response({"message": _("Coupon Created Successfully.")}, status=status.HTTP_201_CREATED)


class CouponDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CouponSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        coupon_id = self.kwargs['coupon_id']

        vendor = Vendor.objects.get(id=vendor_id)

        coupon = Coupon.objects.get(vendor=vendor, id=coupon_id)
        return coupon


class CouponStats(generics.ListAPIView):
    serializer_class = CouponSummarySerializer

    def get_queryset(self):

        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)

        total_coupons = Coupon.objects.filter(vendor=vendor).count()
        active_coupons = Coupon.objects.filter(
            vendor=vendor, active=True).count()

        return [{
            'total_coupons': total_coupons,
            'active_coupons': active_coupons,
        }]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationUnSeenListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (AllowAny, )

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        notifications = Notification.objects.filter(vendor=vendor, seen=False).order_by('seen')
        return notifications
    
class NotificationSeenListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (AllowAny, )

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        notifications = Notification.objects.filter(vendor=vendor, seen=True).order_by('seen')
        return notifications
    
class NotificationSummaryAPIView(generics.ListAPIView):
    serializer_class = NotificationSummarySerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)

        un_read_noti = Notification.objects.filter(vendor=vendor, seen=False).count()
        read_noti = Notification.objects.filter(vendor=vendor, seen=True).count()
        all_noti = Notification.objects.filter(vendor=vendor).count()

        return [{
            'un_read_noti': un_read_noti,
            'read_noti': read_noti,
            'all_noti': all_noti,
        }]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class NotificationMarkAsSeen(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        noti_id = self.kwargs['noti_id']
        vendor = Vendor.objects.get(id=vendor_id)
        notification = Notification.objects.get(vendor=vendor, id=noti_id)
        notification.seen = True
        notification.save()
        return notification
    




class VendorProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny, )



class ShopUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (AllowAny, )      


class ShopAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        vendor_slug = self.kwargs['vendor_slug']

        vendor = Vendor.objects.get(slug=vendor_slug)
        return vendor    


class ShopProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        vendor_slug = self.kwargs['vendor_slug']
        vendor = Vendor.objects.get(slug=vendor_slug)
        products = Product.objects.filter(vendor=vendor)
        return products
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['currency_code'] = self.kwargs.get('currency')
        return context 
    


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        product_instance = serializer.instance

        specifications_data = []
        colors_data = []
        sizes_data = []
        gallery_data = []
        # Loop through the keys of self.request.data      
        for key, value in self.request.data.items():
            # Example key: specifications[0][title]
            if key.startswith('specifications') and '[title_en]' in  key:
            
                # Extract index from key
                index = key.split('[')[1].split(']')[0]
                
                title_en = self.request.data.get(f'specifications[{index}][title_en]')
                title_ar = self.request.data.get(f'specifications[{index}][title_ar]')
                content_en = self.request.data.get(f'specifications[{index}][content_en]')
                content_ar = self.request.data.get(f'specifications[{index}][content_ar]')


                specifications_data.append(
                    {'title_en': title_en,'title_ar': title_ar, 'content_en': content_en,'content_ar': content_ar})

            # Example key: colors[0][name]
            elif key.startswith('colors') and '[name_en]' in key:
                

                index = key.split('[')[1].split(']')[0]

                name_en = self.request.data.get(f'colors[{index}][name_en]')                
                name_ar = self.request.data.get(f'colors[{index}][name_ar]')
                color_code = self.request.data.get(f'colors[{index}][color_code]')

                colors_data.append({'name_en': name_en, 'name_ar': name_ar, 'color_code': color_code,})

            # Example key: sizes[0][name]
            elif key.startswith('sizes') and '[name_en]' in key:
                # Extract index from key
                index = key.split('[')[1].split(']')[0]

                name_en = self.request.data.get(f'sizes[{index}][name_en]')                
                name_ar = self.request.data.get(f'sizes[{index}][name_ar]')
                price_key = f'sizes[{index}][price]'
                price = self.request.data.get(price_key)
                sizes_data.append({'name_en': name_en, 'name_ar': name_ar, 'price': price})

            # Example key: gallery[0][image]
            elif key.startswith('gallery') and '[image]' in key:
                # Extract index from key
                index = key.split('[')[1].split(']')[0]
                image = value
                gallery_data.append({'image': image})

        # Log or print the data for debugging
        

        # Save nested serializers with the product instance
        self.save_nested_data(
            product_instance, SpecificationAddSerializer, specifications_data)
        self.save_nested_data(product_instance, ColorAddSerializer, colors_data)
        self.save_nested_data(product_instance, SizeAddSerializer, sizes_data)
        self.save_nested_data(
            product_instance, GallerySerializer, gallery_data)

    def save_nested_data(self, product_instance, serializer_class, data):
        serializer = serializer_class(data=data, many=True, context={
                                      'product_instance': product_instance})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product_instance)








class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        product_pid = self.kwargs['product_pid']

        vendor = Vendor.objects.get(id=vendor_id)
        product = Product.objects.get(vendor=vendor, pid=product_pid)
        return product

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        product = self.get_object()

        # Deserialize product data
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Delete all existing nested data
        
        product.specification().delete()
        product.color().delete()
        product.size().delete()
        product.gallery().delete()
        # for item in product.gallery:
        #     item.delete()

        specifications_data = []
        colors_data = []
        sizes_data = []
        gallery_data = []
        # Loop through the keys of self.request.data
        for key, value in self.request.data.items():
            # Example key: specifications[0][title]
            if key.startswith('specifications') and '[title_en]' in  key:
            
                # Extract index from key
                index = key.split('[')[1].split(']')[0]
                
                title_en = self.request.data.get(f'specifications[{index}][title_en]')
                title_ar = self.request.data.get(f'specifications[{index}][title_ar]')
                content_en = self.request.data.get(f'specifications[{index}][content_en]')
                content_ar = self.request.data.get(f'specifications[{index}][content_ar]')


                specifications_data.append(
                    {'title_en': title_en,'title_ar': title_ar, 'content_en': content_en,'content_ar': content_ar})

            # Example key: colors[0][name]
            elif key.startswith('colors') and '[name_en]' in key:
                

                index = key.split('[')[1].split(']')[0]

                name_en = self.request.data.get(f'colors[{index}][name_en]')                
                name_ar = self.request.data.get(f'colors[{index}][name_ar]')
                color_code = self.request.data.get(f'colors[{index}][color_code]')

                colors_data.append({'name_en': name_en, 'name_ar': name_ar, 'color_code': color_code,})

            # Example key: sizes[0][name]
            elif key.startswith('sizes') and '[name_en]' in key:
                # Extract index from key
                index = key.split('[')[1].split(']')[0]

                name_en = self.request.data.get(f'sizes[{index}][name_en]')                
                name_ar = self.request.data.get(f'sizes[{index}][name_ar]')
                price_key = f'sizes[{index}][price]'
                price = self.request.data.get(price_key)
                sizes_data.append({'name_en': name_en, 'name_ar': name_ar, 'price': price})

            # Example key: gallery[0][image]
            elif key.startswith('gallery') and '[image]' in key:
                # Extract index from key
                index = key.split('[')[1].split(']')[0]
                image = value
                gallery_data.append({'image': image})

        # Log or print the data for debugging
        

        # Save nested serializers with the product instance
        self.save_nested_data(
            product, SpecificationSerializer, specifications_data)
        self.save_nested_data(product, ColorSerializer, colors_data)
        self.save_nested_data(product, SizeSerializer, sizes_data)
        self.save_nested_data(product, GallerySerializer, gallery_data)

        return Response({'message': _('Product Updated')}, status=status.HTTP_200_OK)

    def save_nested_data(self, product_instance, serializer_class, data):
        serializer = serializer_class(data=data, many=True, context={
                                      'product_instance': product_instance})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product_instance)










class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductAddSerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        vendor = Vendor.objects.get(id=vendor_id)
        products = Product.objects.filter(vendor=vendor)
        return products

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
        product_pid = self.kwargs['product_pid']

        vendor = Vendor.objects.get(id=vendor_id)
        product = Product.objects.get(pid=product_pid, vendor=vendor)
        return product
    def get_complete_image_url(self, image_path):
        # Assuming BASE_URL is defined in your Django settings
        if isinstance(settings.BASE_URL, tuple):
            # Convert tuple to string
            base_url = ''.join(settings.BASE_URL)
        else:
            base_url = settings.BASE_URL
        return base_url + image_path
    

    def get_stats_data(self):
        stats_view = DashboardStatsAPIView()
        stats_view.kwargs = {'vendor_id': self.kwargs['vendor_id']}
        stats_view.request = self.request
        stats_view.format_kwarg = None
        stats_view.format = self.format_kwarg
        stats_view.check_permissions(stats_view.request)
        stats_view.check_object_permissions(stats_view.request, None)
        queryset = stats_view.get_queryset()
        stats_view.list(self.request)
        serializer = stats_view.get_serializer(queryset, many=True)
        return serializer.data[0]
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        # Fetch dashboard statistics
        
        stats_data = self.get_stats_data()




        
        queryset = self.get_queryset()  
        serializer = self.serializer_class(queryset, many=True).data 

        for item in serializer:
                item['image'] = self.get_complete_image_url(item['image'])
                item['category']['image'] = self.get_complete_image_url(item['category']['image'])

     


        return Response({
            "status": "Success",
            "message": _("Product deleted successfully"),
            "dashboard_stats": stats_data,
            "products": serializer,
            
           
        }, status=status.HTTP_200_OK)

