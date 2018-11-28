from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .models import Pizza, Topping, Sub, Extra, Pasta, Salad, Dinner, Item


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
        "dinners": get_menu(Dinner.objects.all()),
        "user": request.user
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

    return render(request, 'orders/login.html', {"message": "Please login with your new account."})

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
        "extra_cheese": Extra.objects.get(name='Extra Cheese')
    }
    return render(request, 'orders/item.html', context)

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

    if request.POST['quantity']:
        quantity = int(request.POST['quantity'])
        price = quantity * item.price

    if item.category.name == 'Pizza':
        try:
            topping1 = Topping.objects.get(pk=request.POST['topping1'])
            print(topping1)
        except:
            pass

        try:
            topping2 = Topping.objects.get(pk=request.POST['topping2'])
            print(topping2)
        except:
            pass

        try:
            topping3 = Topping.objects.get(pk=request.POST['topping3'])
            print(topping3)
        except:
            pass

    if item.category.name == 'Sub':
        try:
            request.POST['extra_cheese']
            price = price + 500
        except:
            pass
    
    print(item.name)
    print(quantity)
    print(price)

    return render(request, 'orders/index.html', {"message": item_id})

@login_required(login_url='/login')
def delete_item(request, item_id):
    return render(request, 'orders/login.html', {"message": item_id})


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