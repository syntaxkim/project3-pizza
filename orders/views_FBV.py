from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from .models import Item, Pizza, Topping, Sub, Extra, Pasta, Salad, Dinner, CartItem, OrderItem, Order

from datetime import datetime


# Create your views here.

# pylint: disable=no-member

def index(request):
    context = {
        "regular_pizzas": get_menu(Pizza.objects.filter(crust='Regular').all()),
        "sicilian_pizzas": get_menu(Pizza.objects.filter(crust='Sicilian').all()),
        "toppings": Topping.objects.all(),
        "subs": get_menu(Sub.objects.all()),
        "extras": Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinners": get_menu(Dinner.objects.all())
    }
    return render(request, 'orders/index.html', context)

def register(request):
    if request.method == 'GET':
        return render(request, 'orders/register.html', {"message": None})

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirmation = request.POST['confirmation']

    # Check forms if valid
    if not username:
        return render(request, 'orders/register.html', {"message": "No username."})
    elif len(username) < 4:
        return render(request, 'orders/register.html', {"message": "Username should be longer than 4 characters."})
    elif not email:
        return render(request, 'orders/register.html', {"message": "No Email."})
    # elif email is not valid:
    #     pass
    elif not password or not confirmation:
        return render(request, 'orders/register.html', {"message": "Type your password."})
    elif len(password) < 8 or len(confirmation) < 8:
        return render(request, 'orders/register.html', {"message": "Password should be longer than 8 characters."})
    elif password != confirmation:
        return render(request, 'orders/register.html', {"message": "Passwords don't match."})
    elif User.objects.filter(email=email):
        return render(request, 'orders/register.html', {"message": "Email is invalid or already taken."})
    else:
        try:
            User.objects.create_user(username, email, password)
        except:
            return render(request, 'orders/register.html', {"message": "Registration failed."})

    return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'GET':
        return render(request, 'orders/login.html', {"message": None})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'orders/login.html', {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, 'orders/login.html', {"message": "Logged out."})

def item(request, item_id):
    context = {
        "item": Item.objects.get(pk=item_id),
        "toppings": Topping.objects.all(),
        "extras": Extra.objects.all()
    }
    return render(request, 'orders/item_detail.html', context)

@login_required(login_url='/login')
def cart_item_list(request):
    cart_list = CartItem.objects.filter(user=request.user).all()
    context = {
        "cart_list": cart_list
    }

    return render(request, 'orders/cartitem_list.html', context)


@login_required(login_url='/login')
def add_item(request, item_id):
    if request.method == 'GET':
        return HttpResponseNotFound()

    try:
        item = Item.objects.get(pk=item_id)
    except KeyError:
        return HttpResponseNotFound()
    except Item.DoesNotExist:
        return HttpResponseNotFound()

    # Get form values
    topping1_id = request.POST.get('topping1', False)
    topping2_id = request.POST.get('topping2', False)
    topping3_id = request.POST.get('topping3', False)
    extra_id = request.POST.get('extra', False)
    quantity = int(request.POST['quantity'])

    price = quantity * item.price

    try:
        cart_item = CartItem.objects.create(user=request.user, item=item, quantity=quantity)

        # If the item has any toppings on it.
        if topping1_id:
            topping1 = Topping.objects.get(pk=topping1_id)
            cart_item.toppings.add(topping1)
        if topping2_id:
            topping2 = Topping.objects.get(pk=topping2_id)
            cart_item.toppings.add(topping2)
        if topping3_id:
            topping3 = Topping.objects.get(pk=topping3_id)
            cart_item.toppings.add(topping3)

        # If the item has extra,
        if extra_id:
            extra = Extra.objects.get(pk=extra_id)
            cart_item.extra = True
            price = price + (quantity * extra.price)

        cart_item.price = price
        cart_item.save()
    except:
        cart_item.delete()
        return HttpResponseNotFound()

    return HttpResponseRedirect(reverse('cart'))

@login_required(login_url='/login')
def order_first(request):
    if request.method == 'GET':
        return HttpResponseNotFound()

    cart_items = CartItem.objects.filter(user=request.user)
    
    # Some sanity checks
    if int(request.POST['user_id']) is not request.user.id:
        return HttpResponseNotFound()
    elif int(request.POST['count_cart_items']) is not len(list(cart_items)):
        return HttpResponseNotFound()

    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.price

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal
    }

    return render(request, 'orders/orderStepFirst.html', context)

@login_required(login_url='/login')
def order_confirm(request):
    if request.method == 'GET':
        return HttpResponseNotFound()

    # Some sanity checks
    if int(request.POST['user_id']) is not request.user.id:
        return HttpResponseNotFound()

    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.price

    context = {
        "subtotal": subtotal,
        "contact": request.POST['contact'],
        "billing_address": request.POST['billing_address'],
        "shipping_address": request.POST['shipping_address'],
        "message": request.POST['message']
    }

    return render(request, 'orders/orderConfirm.html', context)

@login_required(login_url='/login')
def place_order(request):
    if request.method == 'GET':
        return HttpResponseNotFound()

    # Some sanity checks
    if int(request.POST['user_id']) is not request.user.id:
        return HttpResponseNotFound()

    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.price

    contact = request.POST['contact']
    billing_address = request.POST['billing_address']
    shipping_address = request.POST['shipping_address']
    message = request.POST['message']

    try:
        # Create order(a set of order list) object
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            contact=contact,
            billing_address=billing_address,
            shipping_address=shipping_address,
            message=message,
        )
        # Copy data from CartItem to OrderItem
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                user=cart_item.user,
                item=cart_item.item,
                quantity=cart_item.quantity,
                extra=cart_item.extra,
                price=cart_item.price
            )
            for topping in cart_item.toppings.all():
                order_item.toppings.add(topping)
            order.items.add(order_item)
        cart_items.delete() # If everything completed, delete all cart items.
    except:
        return render(request, 'orders/orderResult.html', {"success": False})

    return HttpResponseRedirect(reverse('order_result'))

@login_required(login_url='/login')
def order_result(request):
    return render(request, 'orders/orderResult.html', {"success": True})

@login_required(login_url='/login')
def order_list(request):
    if request.method == 'POST':
        try:
            order_id = request.POST['recieved']
            order = Order.objects.get(pk=order_id, user=request.user)
            order.recieved = True
            order.save()
            return HttpResponseRedirect(reverse('order_list'))
        except:
            return HttpResponseNotFound()

    context = {
        "orders": Order.objects.filter(user=request.user).order_by('-order_time')
    }
    return render(request, 'orders/order_list.html', context)

@login_required(login_url='/login')
def order_detail(request, order_id):
    if request.user.is_superuser:
        order = Order.objects.get(pk=order_id)
    else:
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return HttpResponseNotFound()

    context = {
        "order": order
    }
    return render(request, 'orders/order_detail.html', context)

@login_required(login_url='/login')
def delete_item(request, item_id):
    if request.method == 'GET':
        return HttpResponseNotFound()

    try:
        cart_item = CartItem.objects.get(pk=item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        return HttpResponseNotFound()

    return HttpResponseRedirect(reverse('cart'))

@login_required(login_url='/login')
def manage_order(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    # Update order status.
    if request.method == 'POST':
        try:
            order_id = request.POST['order_id']
            status = request.POST['status']
            order = Order.objects.get(pk=order_id)
            order.status = status
            order.save()
            return HttpResponseRedirect(reverse('manage_order'))
        except:
            return HttpResponseNotFound()

    today = datetime.today()
    context = {
        "today": today,
        "orders": Order.objects.filter(order_time__day=today.day).order_by('-order_time')
    }

    return render(request, 'orders/manageorder_list.html', context)

@login_required(login_url='/login')
def manage_order_detail(request, order_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    # Update order status.
    if request.method == 'POST':
        try:
            order_id = request.POST['order_id']
            status = request.POST['status']
            order = Order.objects.get(pk=order_id)
            order.status = status
            order.save()
            return HttpResponseRedirect(reverse('manage_order_detail'))
        except:
            return HttpResponseNotFound()

    context = {
        "order": Order.objects.get(pk=order_id)
    }
    return render(request, 'orders/manageorder_detail.html', context)

def get_menu(products):
    """List each item with different sizes in a row - name, small, large"""

    # Parse product names
    names = []
    for product in products:
        if product.name not in names:
            names.append(product.name)

    # Parse different sizes with corresponding product name
    items = []
    for name in names:
        item = {}
        item["name"] = name
        for product in products:
            try:                
                if product.name == name and product.size == 'Small':
                    item['id_small'] = product.id
                    item['price_small'] = product.price
                elif product.name == name and product.size == 'Large':
                    item['id_large'] = product.id
                    item['price_large'] = product.price
            # if product has no size attribute (AttributeError)
            except:
                item['id'] = product.id
                item['price'] = product.price
        items.append(item)

    return items