from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .models import Item, Pizza, Topping, Sub, Extra, Pasta, Salad, Dinner, CartItem, OrderItem, Order


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

    if not username:
        return render(request, 'orders/register.html', {"message": "No username."})
    elif not email:
        return render(request, 'orders/register.html', {"message": "No Email."})
    elif not password or not confirmation:
        return render(request, 'orders/register.html', {"message": "Type your password."})
    elif password != confirmation:
        return render(request, 'orders/register.html', {"message": "Passwords don't match."})

    if User.objects.filter(email=email):
        return render(request, 'orders/register.html', {"message": "Email is invalid or already taken."})
    
    try:
        User.objects.create_user(username, email, password)
    except:
        return render(request, 'orders/register.html', {"message": "Unexpected Error."})

    return HttpResponseRedirect(reverse('login_view'))

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
    return render(request, 'orders/item.html', context)

@login_required(login_url='/login')
def cart_list(request):
    cart_list = CartItem.objects.filter(user=request.user).all()
    context = {
        "cart_list": cart_list
    }

    return render(request, 'orders/cart.html', context)


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

    quantity = int(request.POST['quantity'])
    price = quantity * item.price

    try:
        cart_item = CartItem.objects.create(user=request.user, item=item, quantity=quantity)
    except:
        return HttpResponseNotFound()

    if item.category.name == 'Pizza':
        try:
            topping1 = Topping.objects.get(pk=request.POST['topping1'])
            cart_item.toppings.add(topping1)
        except:
            pass

        try:
            topping2 = Topping.objects.get(pk=request.POST['topping2'])
            cart_item.toppings.add(topping2)
        except:
            pass

        try:
            topping3 = Topping.objects.get(pk=request.POST['topping3'])
            cart_item.toppings.add(topping3)
        except:
            pass

    if item.category.name == 'Sub':
        try:
            extra = Extra.objects.get(pk=request.POST['extra'])
            price = price + (quantity * extra.price)
            cart_item.extra = True
        except:
            pass

    cart_item.price = price
    cart_item.save()

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

    return render(request, 'orders/orderResult.html', {"success": True})

@login_required(login_url='/login')
def order_list(request):
    if request.method == 'POST':
        try:
            order_id = request.POST['recieved']
            order = Order.objects.get(pk=order_id, user=request.user)
            order.recieved = True
            order.save()
        except:
            return HttpResponseNotFound()

    context = {
        "orders": Order.objects.filter(user=request.user)
    }
    return render(request, 'orders/orderList.html', context)

@login_required(login_url='/login')
def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
    except Order.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        "order": order
    }
    return render(request, 'orders/orderDetail.html', context)

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