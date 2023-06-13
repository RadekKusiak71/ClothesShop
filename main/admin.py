from django.contrib import admin
from .models import Cart,Product,Order,OrderItem,CartItem,Category,Order_details

admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Order_details)