from django.urls import path

from userauths import views as userauths_views
from rest_framework_simplejwt.views import TokenRefreshView
from store import views as store_views
from customer import views as customer_views
urlpatterns = [
    path('user/token/', userauths_views.MyTokenOptainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', userauths_views.RegisterView.as_view()),
    path('user/password-reset/<email>/', userauths_views.PasswordRestEmailVerify.as_view()),
    path('user/password-change/', userauths_views.PasswordChangeView.as_view()),
    path('user/profile/<user_id>/', userauths_views.ProfileView.as_view()),

    # Store Endpoint
    path('productss/', store_views.Fpro.as_view()),



    path('category/', store_views.CategoryListAPIView.as_view()),
    path('brand/', store_views.BrandListAPIView.as_view()),
    path('product/', store_views.ProductListAPIView.as_view()),
    path('product/<slug:slug>/', store_views.ProductDetailAPIView.as_view()),
    path('product/category/<str:category>/',store_views.ProductCategory.as_view()),
    path('reviews/',store_views.ReviewListAPIView.as_view()),
    path('reviews/<product_id>/',store_views.ReviewListAPIView.as_view()),
    #path('reviews/summary/<product_id>/',store_views.ReviewSummaryAPIView.as_view()),

    path('product/brand/<str:brand>/',store_views.ProductBrandListAPIView.as_view()),



    path('cart-view/', store_views.CartAPIView.as_view()),
    path('cart-list/<str:cart_id>/<int:user_id>/', store_views.CartListView.as_view()),
    path('cart-list/<str:cart_id>/', store_views.CartListView.as_view()),
    path('cart-detail/<str:cart_id>/<int:user_id>/', store_views.CartDetailView.as_view()),
    path('cart-detail/<str:cart_id>/', store_views.CartDetailView.as_view()),


    path('cart-delete/<str:cart_id>/<int:item_id>/<int:user_id>/',store_views.CartItemDeleteAPIView.as_view()),
    path('cart-delete/<str:cart_id>/<int:item_id>/',store_views.CartItemDeleteAPIView.as_view()),
    path('create-order/',store_views.CreateOrderAPIView.as_view()),
    path('checkout/<order_oid>/',store_views.CheckoutView.as_view()),
    path('coupon/',store_views.CouponAPIView.as_view()),

    #payments
    path('stripe-checkout/<order_oid>/<cart_id>/',store_views.StripeCheckoutView.as_view()),
    path('payment-success/<order_oid>/',store_views.PaymentSuccessView.as_view()),

    #Customer Endpoint
    path('customer/orders/<user_id>/',customer_views.OrderAPIView.as_view()),
    path('customer/orders/<user_id>/<order_oid>/',customer_views.OrderDetailAPIView.as_view()),
    #path('customer/wishlist/<user_id>/',customer_views.WishListAPIView.as_view()),
    path('customer/wishlist/create/', customer_views.WishlistCreateAPIView.as_view(), name='customer-wishlist-create'),
    path('customer/wishlist/<user_id>/', customer_views.WishlistAPIView.as_view(), name='customer-wishlist'),
    path('customer/notifications/<user_id>/',customer_views.NotificationListAPIView.as_view()),
    path('customer/notifications/<user_id>/<noti_id>/',customer_views.MarkCustomerNotificationAsSeen.as_view()),


]
