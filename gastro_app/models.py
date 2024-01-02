from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True) #Change during status becomes 'In delivery'

class MenuItem(models.Model):
    #Initially im limiting app to one restaurant but leaving Restaurant and MenuItem relationship in case of further development
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=512, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #image = models.ImageField

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('In delivery', 'In delivery'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='Pending')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    
    #Add function that checks if the status is changing to 'In Delivery' and updates 'is_available' status of the supplier associated to this order

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    

