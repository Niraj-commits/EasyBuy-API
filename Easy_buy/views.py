from django.shortcuts import render,HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permission import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import filters
from .filter import *
from .pagination import *
from rest_framework import status
from drf_spectacular.utils import extend_schema,OpenApiExample

@extend_schema(
    tags=['Category'],
    examples=[
        OpenApiExample(
        "Simple Category Example",
        value={
            "name":"category"
        }
    )]
)
class CategoryViewset(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]
    filter_backends = [filters.SearchFilter,filter.DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = CategoryFilter
    pagination_class = CustomPagination
    
    def destroy(self,request,pk):
        queryset = Category.objects.get(pk = pk)
        occurence = Product.objects.filter(category = queryset).exists()
        
        if occurence:
            raise serializers.ValidationError({"Details":"Cannot Delete Category is in use"},status= status.HTTP_226_IM_USED) 
        queryset.delete()
        return Response({"Details":"Category has been deleted"},status=status.HTTP_200_OK)
        
@extend_schema(
    tags=['Product'],
    examples=[
        OpenApiExample(
            "Simple Product Example",
            value={
                "name":"product",
                "description":"description",
                "amount":1,
                "quantity":4,
                "category":1,
            }
        )]
)

class ProductViewset(viewsets.ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductViewPermission]
    filter_backends = [filters.SearchFilter,filter.DjangoFilterBackend]
    search_fields = ['name','category__name','price'] # To Search from a Foreign key need to specify field inside related model
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    
    
    def destroy(self, request,pk):
        queryset = Product.objects.get(pk = pk)
        ordered_item = OrderItem.objects.filter(product = queryset).exists()
        purchased_item = Purchase_Item.objects.filter(product = queryset).exists()
        
        if ordered_item:
            raise serializers.ValidationError({"Details":"Product is ordered can't delete"},status = status.HTTP_226_IM_USED)
        
        if purchased_item:
            raise serializers.ValidationError({"Details":"Product is purchased can't delete"},status = status.HTTP_226_IM_USED)
        
        queryset.delete()
        return Response({"Details":"Product Deleted Successfully"},status=status.HTTP_200_OK)

class OrderViewset(viewsets.ModelViewSet):
    
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter,filter.DjangoFilterBackend]
    search_fields = ['customer__username','status']
    filterset_class = OrderFilter
    pagination_class = CustomPagination
    permission_classes = [OrderPermission]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Order.objects.all()

        return Order.objects.filter(customer=user) #shows only their orders 
    
    def destroy(self, request,pk):
        queryset = Order.objects.get(pk = pk)
        ordered_item = OrderItem.objects.filter(order = queryset).exists()
        delivery = OrderDelivery.objects.filter(order = queryset).exists()
        
        if ordered_item:
            raise serializers.ValidationError({"Details":"Order has order items remove them first"},status = status.HTTP_400_BAD_REQUEST)
        if delivery:
            raise serializers.ValidationError({"Details":"Order has been assigned remove them first"},status = status.HTTP_400_BAD_REQUEST)

        queryset.delete()
        return Response({"Details":"Order has been deleted"},status= status.HTTP_200_OK)
        
        
class OrderItemViewset(viewsets.ModelViewSet):
    
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderDeliveryViewset(viewsets.ModelViewSet):
    
    queryset = OrderDelivery.objects.all()
    serializer_class = OrderDeliverySerializer
    permission_classes = [AssignOrderDelivery]
    filter_backends = [filters.SearchFilter,filter.DjangoFilterBackend]
    search_fields = ['delivery__username','status','order']
    filterset_class = OrderDeliveryFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return OrderDelivery.objects.all()

        return OrderDelivery.objects.filter(delivery=user) #only shows deliveries assigned to them

class PurchaseItemViewset(viewsets.ModelViewSet):
    
    queryset = Purchase_Item.objects.all()
    serializer_class = PurchaseItemSerializer

class PurchaseViewset(viewsets.ModelViewSet):
    
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [filters.SearchFilter,filter.DjangoFilterBackend]
    search_fields = ['supplier__username','status']
    filterset_class = PurchaseFilter
    pagination_class = CustomPagination
    permission_classes = [PurchasePermission]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == "admin":
            return Purchase.objects.all()
        
        elif user.role == "supplier":
            
            return Purchase.objects.filter(supplier = user)
    
    def destroy(self, request, pk):
        queryset = Purchase.objects.get(pk = pk)
        purchased_item = Purchase_Item.objects.filter(purchase = queryset).exists()
        delivery = PurchaseDelivery.objects.filter(purchase = queryset).exists()
        
        if purchased_item:
            raise serializers.ValidationError({"Details":"Purchase contains items remove them first"},status = status.HTTP_400_BAD_REQUEST)
        
        if delivery:
            raise serializers.ValidationError({"Details":"Purchase has been assigned remove them first"},status = status.HTTP_400_BAD_REQUEST)
        
        queryset.delete()
        
        return Response({"Details":"Deleted Purchase Successfully"})
        
class PurchaseDeliveryViewset(viewsets.ModelViewSet):
    
    queryset = PurchaseDelivery.objects.all()
    serializer_class = PurchaseDeliverySerializer
    permission_classes = [AssignPurchaseDelivery]
    filter_backends = [filters.SearchFilter,filter.DjangoFilterBackend]
    search_fields = ['delivery__username','status','purchase']
    filterset_class = PurchaseDeliveryFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return PurchaseDelivery.objects.all()

        return PurchaseDelivery.objects.filter(delivery=user)

class AdminDashboard(ViewSet):
    
    permission_classes = [AdminDashboardView]
    def list(self,request):
        total_spent = 0
        best_spent = 0
        best_customer = None
        total_sold = 0
        total_ordered = 0
        best_supplier = None
        best_supplied = 0
        profit = 0
        customers = User.objects.filter(role = "customer")
        suppliers = User.objects.filter(role = "supplier")
        
        # For Best Customer
        for customer in customers:
            total_spent = 0 
            for orders in customer.order_set.all():
                if orders.status == "completed":
                    order_total = 0
                    for order_items in orders.items.all():
                        price = order_items.product.price
                        quantity = order_items.quantity
                        order_total += price * quantity
                    total_spent += order_total
                    total_sold += order_total
            
            if total_spent > best_spent:
                best_spent = total_spent
                best_customer = customer.username      
        
        # For Best Supplier
        total_supplied = 0
        for supplier in suppliers:
            for purchase in supplier.purchase_set.all():
                if purchase.status == "completed":
                    for purchase_item in purchase.items.all():
                        
                        price = purchase_item.product.price
                        quantity = purchase_item.quantity
                        supply_total = price * quantity
                        total_supplied += quantity
                        total_ordered += supply_total
            
            if total_supplied > best_supplied:
                best_supplied = total_supplied
                best_supplier = supplier.username
        
            profit = total_sold - total_ordered
        
        stats = {
            "total_users": User.objects.count(),
            "customers": User.objects.filter(role = "customer").count(),
            "suppliers": User.objects.filter(role = "supplier").count(),
            "deliverers": User.objects.filter(role = "delivery").count(),
            "admins":User.objects.filter(role = "admin").count(),
            "best_customer":best_customer,
            "total_spent_by_best_customer":total_spent,
            "best_supplier":best_supplier,
            "total_supplied_by_best_supplier":total_supplied,
            "total_ordered":total_ordered,
            "total_revenue": total_sold,
            "profit/loss": profit,
            "orders_pending":Order.objects.filter(status = "pending").count(),
            "orders_completed":Order.objects.filter(status = "completed").count(),
            "orders_cancelled":Order.objects.filter(status = "cancelled").count(),
        }
        return Response(stats)


class SupplierDashboard(ViewSet):
    
    permission_classes = [SupplierDashboardView]
    
    def list(self,request):
        low_stock_products = Product.objects.filter(quantity__lte=5) #filtering values less than equal to 5 quantity
        
        stats = {
            "Low Stock Product Count":low_stock_products.count(),
            "Low Stock Products":list(low_stock_products.values('id','name','quantity')),
            "Deliveries Pending": Purchase.objects.filter(status = "pending").count(),
            "Deliveries Completed": Purchase.objects.filter(status = "completed").count(),
            "Deliveries Cancelled":Purchase.objects.filter(status = "cancelled").count()
        }
        return Response (stats)