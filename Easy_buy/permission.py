
from rest_framework.permissions import BasePermission,SAFE_METHODS

class ProductViewPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user or not request.user.is_authenticated :
            return False
        
        if request.user.role == "admin":
            return True
        
        elif request.user.role == "customer":
            if request.method in SAFE_METHODS:
                return True
            else:
                return False
        
        elif request.user.role == "supplier":
            if request.method in SAFE_METHODS: #or request.method in "POST":
                return True
            else:
                return False
class CategoryPermission(BasePermission):
    
    def has_permission(self,request,view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        elif request.user.role == "admin":
            return True
        
        else:
            return False
        
class AssignOrderDelivery(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        else:
            if request.user.role == "admin":
                return True
            
            elif request.user.role == "delivery":
                if request.method in SAFE_METHODS or request.method in "PATCH":
                    return True
                else:
                    return False

class AssignPurchaseDelivery(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        else:
            if request.user.role == "supplier":
                return True
            
            elif request.user.role == "delivery": #or request.user.role == "admin":
                if request.method in SAFE_METHODS or request.method in "PATCH":
                    return True
                else:
                    return False

class SupplierDashboardView(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        else:
            if request.user.role == "admin" or request.user.role == "supplier": 
                return True
            
            else:
                return False

class AdminDashboardView(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        else:
            if request.user.role == "admin": 
                return True
            
            else:
                return False

class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role =="admin":
            # if request.method in SAFE_METHODS:
                return True
            # else:
            #     return False
        elif request.user.role == "customer":
            if request.method in SAFE_METHODS or request.method in "POST":
                return True
            else:
                return False
        
        else:
            return False

class PurchasePermission(BasePermission):
    
    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == "supplier":
            if request.method in SAFE_METHODS or request.method in "POST":
                return True
            
            else :
                return False
        
        elif request.user.role == "admin":
            
            if request.method in SAFE_METHODS or request.method in "PATCH":
                return True
            else:
                return False