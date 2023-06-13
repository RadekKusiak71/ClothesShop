from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from datetime import date
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='main/product_image/')
    sales = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.price}$' 
    
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.owner:
            return f'Cartf for user {self.owner}'
        else:
            return f'Cart for {self.session_key}'
        
class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name    

class Order(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.owner:
            return f'Order for user: {self.owner} - number : {self.id}'
        else:
            return f'Order {self.session_key} - {self.id}'

class Order_details(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False,null=True,blank=True)
    order = models.ForeignKey('Order',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'Order number {self.id} for {self.first_name} - {self.last_name}'

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)


    def __str__(self):
        if self.order.owner:
            return f"{self.order.owner} - {self.product.name}"
        else:
            return f"{self.order.session_key} - {self.product.name}"