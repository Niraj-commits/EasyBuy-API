from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('login',LoginView,basename='login')
router.register('register_admin',AdminRegisterView,basename='admin')
router.register('register_customer',CustomerRegisterView,basename='customer')
router.register('register_supplier',SupplierRegisterView,basename='supplier')
router.register('register_deliverer',DeliveryRegisterView,basename='deliverer')

urlpatterns = [
    path('',include(router.urls))
]
