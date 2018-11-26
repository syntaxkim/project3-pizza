from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Pizza, Topping, Sub, Pasta, Salad, Dinner


# Create your views here.
# pylint: disable=no-member
# @login_required(login_url='/login')
def index(request):
    context = {
        "regular_pizzas": get_menu(Pizza.objects.filter(crust='Regular').all()),
        "sicilian_pizzas": get_menu(Pizza.objects.filter(crust='Sicilian').all()),
        "toppings": get_menu(Topping.objects.all()),
        "subs": get_menu(Sub.objects.all()),
        "pastas": get_menu(Pasta.objects.all()),
        "salads": get_menu(Salad.objects.all()),
        "dinners": get_menu(Dinner.objects.all()),
        "user": request.user
    }
    return render(request, 'orders/index.html', context)

def register_view(request):
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