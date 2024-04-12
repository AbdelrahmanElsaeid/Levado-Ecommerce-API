
from django.shortcuts import render,redirect
from store.models import Category,Product,Cart,Tax,CartOrder,CartOrderItem,Coupon,Notification,Review,Wishlist
from store.serializer import CartSerializer, ProductDetailSerializer,CategorySerializer,CartOrderSerializer,WishlistListSerializer,NotificationSerializer,ReviewSerializer,WishlistSerializer
from rest_framework import generics,status
from rest_framework.permissions import AllowAny 
from userauths.models import User
from decimal import Decimal
from rest_framework.response import Response
# Create your views here.

class OrderAPIView(generics.ListAPIView):
    serializer_class=CartOrderSerializer
    permission_classes=[AllowAny,]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        orders = CartOrder.objects.filter(buyer=user, payment_status = "paid")

        return orders
    

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class=CartOrderSerializer
    permission_classes=[AllowAny,]

    def get_object(self):
        user_id = self.kwargs['user_id']
        order_oid = self.kwargs['order_oid']
        user = User.objects.get(id=user_id)

        orders = CartOrder.objects.get(buyer=user,oid=order_oid, payment_status = "paid")

        return orders    
    


# class WishlistCreateAPIView(generics.CreateAPIView):
#     serializer_class = WishlistSerializer
#     permission_classes = (AllowAny, )

#     def create(self, request):
#         payload = request.data 

#         product_id = payload['product_id']
#         user_id = payload['user_id']

#         user = User.objects.get(id=user_id)
#         wishlist_data = Wishlist.objects.filter(user=user,)
#         serialized_wishlist_data = self.serializer_class(wishlist_data, many=True).data

#         try:
#             product = Product.objects.get(id=product_id)
#             user = User.objects.get(id=user_id)
#         except (Product.DoesNotExist, User.DoesNotExist):
#             return Response({"message": "User or Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

#         wishlist_exists = Wishlist.objects.filter(product=product, user=user).exists()
#         if wishlist_exists:
#             Wishlist.objects.filter(product=product, user=user).delete()
#             user_wishlist = Wishlist.objects.filter(user=user)
#             serialized_wishlist = self.serializer_class(user_wishlist, many=True).data
#             return Response({"message": "Removed From Wishlist", "wishlist": serialized_wishlist, "data": serialized_wishlist_data}, status=status.HTTP_200_OK)
#         else:
#             wishlist = Wishlist.objects.create(product=product, user=user)
#             user_wishlist = Wishlist.objects.filter(user=user)
#             serialized_wishlist = self.serializer_class(user_wishlist, many=True).data
#             return Response({"message": "Added To Wishlist", "wishlist": serialized_wishlist, "data": serialized_wishlist_data}, status=status.HTTP_201_CREATED)
from django.shortcuts import get_object_or_404
class WishlistCreateAPIView(generics.CreateAPIView):
    serializer_class = WishlistListSerializer
    permission_classes = (AllowAny, )

    def get_user_wishlist_product_ids(self, user):
        user_wishlist = Wishlist.objects.filter(user=user)
        return list(user_wishlist.values_list('product_id', flat=True))
    
    def get_user_wishlist_product(self, user):
        user_wishlist = Wishlist.objects.filter(user=user)
        return user_wishlist

    def create(self, request):
        payload = request.data 
        product_id = payload.get('product_id')
        user_id = payload.get('user_id')

        if not product_id or not user_id:
            return Response({"message": "Product ID and User ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        wishlist_exists = Wishlist.objects.filter(product=product, user=user).exists()

        if wishlist_exists:
            Wishlist.objects.filter(product=product, user=user).delete()
            message = "Removed From Wishlist"
        else:
            Wishlist.objects.create(product=product, user=user)
            message = "Added To Wishlist"

        wishlist_product_ids = self.get_user_wishlist_product_ids(user)

        wishlist_data = self.get_user_wishlist_product(user)

        serialized_wishlist = self.serializer_class(wishlist_data, many=True).data


        

        return Response({"message": message, "wishlist": wishlist_product_ids, "data": serialized_wishlist}, status=status.HTTP_200_OK if wishlist_exists else status.HTTP_201_CREATED)



class WishlistAPIView(generics.ListAPIView):
    serializer_class = WishlistListSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        wishlist = Wishlist.objects.filter(user=user,)
        return wishlist
    




class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes=[AllowAny,]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        notif = Notification.objects.filter(user=user, seen=False)

        return notif



class MarkCustomerNotificationAsSeen(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes=[AllowAny,]

    def get_object(self):
        user_id = self.kwargs['user_id']
        noti_id = self.kwargs['noti_id']

        user = User.objects.get(id=user_id)
        noti = Notification.objects.get(id=noti_id, user=user)

        if noti.seen != True:
            noti.seen = True
            noti.save()

        return noti