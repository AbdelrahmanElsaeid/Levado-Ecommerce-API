from django.shortcuts import render
from django.conf import settings
from .models import User, Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer ,RegisterSerializer, UserSerializer,ProfileSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
import random
import shortuuid

# Create your views here.


class MyTokenOptainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        tokens = serializer.validated_data
        response_data = {
            'tokens': tokens,
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'username': user.username,
                # Add more user information as needed
            }
        }
        return Response(response_data)



    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = RegisterSerializer 


    def create(self, request, *args, **kwargs):
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            return Response({'message': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        user = User.objects.create(
            full_name=serializer.validated_data['full_name'],
            email=email,
            phone=serializer.validated_data['phone'], 
        )  
        email_user, _ = email.split("@")
        user.username = email_user
        user.set_password(serializer.validated_data['password'])
        user.save()


def generate_otp():
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:6]
    return unique_key

# class PasswordRestEmailVerify(generics.RetrieveAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny, )

#     def get_object(self):
#         email = self.kwargs['email']
#         user = User.objects.get(email=email)

#         if user:
#             user.otp= generate_otp()
#             user.save()

#             uidb64 = user.pk
#             otp = user.otp

#             link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"
#             print(link)

#         return user   

from django.core.mail import send_mail
from django.urls import reverse
class PasswordRestEmailVerify(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp= generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp

            link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"
            # print(link)
            #link = reverse('create-new-password') + f'?otp={otp}&uidb64={uidb64}'

            email_subject = 'Reset Your Password'
            email_body = f'Please follow this link to reset your password: {link}'

            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            

        return user    


class PasswordChangeView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )        

    def create(self,request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uidb64 = payload['uidb64']
        password = payload['password']

        user = User.objects.get(otp=otp, id=uidb64)

        if user:
            user.set_password(password)
            user.otp= ""
            user.save()
            return Response({"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)





class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes = [AllowAny,]

    def get_object(self):
        user_id = self.kwargs['user_id']

        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)

        return profile