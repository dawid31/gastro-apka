from django.shortcuts import render
from .models import Product, Cart, CartItem, Order, OrderItem, OrderStatus
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu')
    return render(request, 'gastro_app/login.html')


def index(request):
    return render(request, 'gastro_app/index.html')


def menu(request):
    products = Product.objects.all()
    # username = "dawid"  # Replace with the actual username
    # user = get_object_or_404(User, username=username)
    # user_cart = get_object_or_404(Cart, user=user)
    # cart_items = user_cart.cartitem_set.all()
    context = {'products': products}
    return render(request, 'gastro_app/menu.html', context)

def userCart(request, pk):
    user = User.objects.get(id=pk)
    user_cart = get_object_or_404(Cart, user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_price = user_cart.calculate_total_price()

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'gastro_app/cart.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    # Get or create the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    # If the cart item already exists, ensure quantity is set to at least 1
    if not created and cart_item.quantity is None:
        cart_item.quantity = 1
    elif not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('menu')  # Change 'product_list' to the name of your product list view

def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    # Get the user's cart
    user_cart = request.user.cart

    # Check if the product is in the cart
    try:
        cart_item = CartItem.objects.get(cart=user_cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Product not in the cart, do nothing

    return redirect('cart', pk=request.user.id)

def place_order(request):
    if request.method == 'POST':
        # Pobierz produkty z koszyka użytkownika
        user_cart = request.user.cart
        cart_items = user_cart.cartitem_set.all()

        # Utwórz nowe zamówienie
        order = Order.objects.create(user=request.user, total_price=user_cart.calculate_total_price())

        # Dodaj produkty do zamówienia
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

        # # Ustaw status zamówienia na "Przyjęte"
        # order_status = OrderStatus.objects.get(name="Przyjęte")
        # order.status = order_status
        # order.save()

        # Wyczyść koszyk użytkownika
        user_cart.cartitem_set.all().delete()

        #messages.success(request, 'Zamówienie zostało złożone pomyślnie!')
        return redirect('order_status', order_id=order.id)

    return render(request, 'gastro_app/place_order.html')

def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'gastro_app/order_status.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')  # Redirect to your desired page
    else:
        form = UserCreationForm()
    context = {'form': form}

    return render(request, 'gastro_app/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('menu')  # Redirect to your desired page
