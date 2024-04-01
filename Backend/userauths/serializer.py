from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import IntegrityError

from .models import User, Profile
from django.contrib.auth.password_validation import validate_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        try:
            token['vendor_id'] = user.vendor.id
        except:
            token['vendor_id'] = 0

        return token 


def validate_phone_number(value):
    if not value.startswith('01'):
        raise serializers.ValidationError({'phone':'Phone number must start with "01".'})
    
def validate_full_name(value):
    if len(value) < 3:
        raise serializers.ValidationError({'full_name': 'Full name must be at least 3 characters long.'})
    elif len(value) > 30:
        #raise serializers.ValidationError({'full_name': 'Full name cannot be longer than 30 characters.'})
        return Response({'message': 'Full name cannot be longer than 30 characters.'}, status=status.HTTP_400_BAD_REQUEST)
def validate_email(value):
    if User.objects.filter(email=value).exists():
        return Response({'message': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)


    def validate_full_name_and_phone(self, attrs):
        full_name = attrs.get('full_name')
        phone = attrs.get('phone')
        email = attrs.get('email')
        validate_email(email)
        validate_full_name(full_name)
        validate_phone_number(phone)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password', 'password2']

    def validate(self, attrs):
        self.validate_full_name_and_phone(attrs)
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'message': 'Password does not match'})
            #return Response({'Message': 'Password does not match'}, status=status.HTTP_400_BAD_REQUEST)

    
        
        
        return attrs
        
      


    # def create(self, validated_data):
    #     value=validated_data['email'],

    #     if User.objects.filter(email=value).exists():
    #         return Response({'Message': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
       
    #     else:
    #         user = User.objects.create(
    #             full_name=validated_data['full_name'],
    #             email=validated_data['email'],
    #             phone=validated_data['phone'], 
    #         )  
    #         email_user,_ = user.email.split("@")
    #         user.username = email_user
    #         user.set_password(validated_data['password'])

    #         user.save()
    #         return user     


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


    def to_representation(self, instance):
        response =  super().to_representation(instance) 
        response['user'] = UserSerializer(instance.user).data
        return response   
    


class ProfileReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id','full_name', 'image']