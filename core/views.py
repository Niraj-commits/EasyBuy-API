from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view,extend_schema,OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .permission import *
# Create your views here.

class AdminRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="admin")
    serializer_class = AdminSerializer
    permission_classes = [RegisterUser]
    
class CustomerRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="customer")
    serializer_class = CustomerSerializer
    permission_classes = [RegisterUser]

class SupplierRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="supplier")
    serializer_class = SupplierSerializer
    permission_classes = [RegisterUser]

class DeliveryRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="delivery")
    serializer_class = DeliverySerializer
    permission_classes = [RegisterUser]

class LoginView(viewsets.ViewSet):
    
    @extend_schema(
        request= LoginSerializer,
        responses = {200:LoginSerializer},
        methods = ['POST']
    )
    
    def create(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username == None and password == None:
            raise serializers.ValidationError({"Details":"Sorry fields cannot be empty"})
        
        data = authenticate(username = username,password = password)
        
        if data:
            token,_ = Token.objects.get_or_create(user = data)
            return Response({
                "token":token.key,
                "user":username,
            })
        
        else:
            raise serializers.ValidationError({"Details":"Wrong Credentials"})