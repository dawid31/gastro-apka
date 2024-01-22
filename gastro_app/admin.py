from django.contrib import admin
from .models import Restaurant, Product, Order, OrderItem, CartItem, Cart, Client, OrderStatus

admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Client)
admin.site.register(OrderStatus)