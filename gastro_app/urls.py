from django.urls import path
from .views import login
from .views import index

urlpatterns = [
    path('login/', login, name='login'),
    path('', index, name='index')
]