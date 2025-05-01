from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.utils import timezone
# Create your models here.

STATE_CHOICES=(
('AP', 'Andhra Pradesh'),
('AR', 'Arunachal Pradesh'),
('AS', 'Assam'),
('BR', 'Bihar'),
('CG', 'Chhattisgarh'),
('GA', 'Goa'),
('GJ', 'Gujarat'),
('HR', 'Haryana'),
('HP', 'Himachal Pradesh'),
('JH', 'Jharkhand'),
('KA', 'Karnataka'),
('KL', 'Kerala'),
('MP', 'Madhya Pradesh'),
('MH', 'Maharashtra'),
('MN', 'Manipur'),
('ML', 'Meghalaya'),
('MZ', 'Mizoram'),
('NL', 'Nagaland'),
('OR', 'Odisha'),
('PB', 'Punjab'),
('RJ', 'Rajasthan'),
('SK', 'Sikkim'),
('TN', 'Tamil Nadu'),
('TS', 'Telangana'),
('TR', 'Tripura'),
('UP', 'Uttar Pradesh'),
('UK', 'Uttarakhand'),
('WB', 'West Bengal')

)
CATEGORY_CHOICES=(
    ('H','Herb'),
    ('S','Shrub'),
    ('T','trees'),
    ('Cmb','Climber'),
    ('Cpr','Creeper'),
    ('FP','Flowering Plants'),
    ('AG','Agro'),
    ('Seed','Seed'),
    ('Soil','Soil'),
    ('Tool','Tool'),
    
)

class Product(models.Model):
    title = models.CharField(max_length=100)

    selling_price = models.FloatField()

    discounted_price = models.FloatField(null=True,blank=True)

    botanical_name = models.TextField(max_length=100,blank=True)

    weather = models.TextField(max_length=500,default=' ')

    How_to_Handle_Tips = models.TextField(max_length=500,default=' ')

    proadd = models.TextField(default='')

    category = models.CharField(choices=CATEGORY_CHOICES,max_length=50)

    product_image = models.ImageField(upload_to='product/')
    def __str__(self) :
        return self.title
    

class Category(models.Model):
    title = models.CharField(choices=CATEGORY_CHOICES,max_length=50)
    def __str__(self):
        return dict(CATEGORY_CHOICES).get(self.title, self.title)


from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex='^\d{10}$', message='Mobile number must be exactly 10 digits.')
        ]
    )
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(regex='^\d{6}$', message='Pincode must be exactly 6 digits.')
        ]
    )
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return self.name

     
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)  
    quantity =models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)

    @property
    def total_cost(self):
        return self.product.discounted_price * self.quantity
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem', blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ))

    def __str__(self):
        return f"Order {self.id} - {self.user}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    product =models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'product')

class VisitHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)       
            



