from django.shortcuts import render

from .models import User, Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer ,RegisterSerializer, UserSerializer
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
            print(link)

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
