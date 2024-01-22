from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('menu/', views.menu, name='menu'),
    path('cart/<str:pk>/', views.userCart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_status/<int:order_id>/', views.order_status, name='order_status'),
    path('restaurant/orders/', views.restaurant_order_list, name='restaurant_order_list'),
    path('restaurant/orders/<int:order_id>/change-status/', views.change_order_status, name='change_order_status'),
]