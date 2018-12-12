from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView, ListView, DeleteView, RedirectView
from django.db.models import Q

from .models import Item, Pizza, Topping, Sub, Extra, Pasta, Salad, Dinner, CartItem, OrderItem, Order

from datetime import datetime


# Create your views here.

# pylint: disable=no-member

class IndexView(TemplateView):
    template_name = 'orders/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        return context

class ItemDetail(DetailView):
    model = Item
    extra_context = {
        "toppings": Topping.objects.all(),
        "extras": Extra.objects.all()
    }

class CartItemList(ListView):
    model = CartItem
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartitem_list = CartItem.objects.filter(user=self.request.user).all()
        subtotal = 0
        for cartitem in cartitem_list:
            subtotal += cartitem.price
        context = {
            "cartitem_list": cartitem_list,
            "subtotal": subtotal
        }
        return context

class AddItem(View):
    model = Item

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs['pk'])
        
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
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return HttpResponseRedirect(reverse('cart'))

class DeleteItem(DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart')

@login_required(login_url='/login')
def order_first(request):
    if request.method == 'GET':
        return HttpResponseNotFound('<h1>Page not found</h1>')

    cartitem_list = CartItem.objects.filter(user=request.user)
    
    # Some sanity checks
    if int(request.POST['user_id']) is not request.user.id:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    elif int(request.POST['count_cart_items']) is not len(cartitem_list):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    subtotal = 0
    for cartitem in cartitem_list:
        subtotal += cartitem.price

    context = {
        "cartitem_list": cartitem_list,
        "subtotal": subtotal
    }

    return render(request, 'orders/orderStepFirst.html', context)

@login_required(login_url='/login')
def order_confirm(request):
    if request.method == 'GET':
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # Some sanity checks
    if int(request.POST['user_id']) is not request.user.id:
        return HttpResponseNotFound('<h1>Page not found</h1>')

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
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # Some sanity checks
    if int(request.POST['user_id']) is not request.user.id:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.price

    # Get form data
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

class OrderList(ListView):
    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user).order_by('-order_time')
        return orders

    def post(self, request):
        try:
            # Update recieved status.
            order_id = request.POST['recieved']
            order = Order.objects.get(pk=order_id, user=request.user)
            order.recieved = True
            order.save()
            return HttpResponseRedirect(reverse('order_list'))
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

class OrderDetail(DetailView):
    model = Order

    def get_object(self):
        order = Order.objects.get(pk=self.kwargs['pk'], user=self.request.user)    
        return order

class ManageOrder(PermissionRequiredMixin, ListView):
    permission_required = 'orders.can_manage'
    model = Order
    template_name = 'orders/manageorder_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        context["today"] = today
        context["order_list_not_recieved"] = Order.objects.filter(Q(order_time__day=today.day)|Q(recieved=False)).order_by('-order_time')
        return context

    def post(self, request, *args, **kwargs):
        try:
            # Update order status.
            order_id = request.POST['order_id']
            status = request.POST['status']
            order = Order.objects.get(pk=order_id)
            order.status = status
            order.save()
            return HttpResponseRedirect(reverse('manage_order'))
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

class ManageOrderDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'orders.can_manage'
    model = Order
    template_name = 'orders/manageorder_detail.html'

    def post(self, request, *args, **kwargs):
        try:
            # Update order status.
            order_id = request.POST['order_id']
            status = request.POST['status']
            order = Order.objects.get(pk=order_id)
            order.status = status
            order.save()
            return HttpResponseRedirect(reverse('manage_order_detail'))
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

def register(request):
    if request.method == 'GET':
        return render(request, 'orders/register.html', {"message": None})

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirmation = request.POST['confirmation']

    # Server-side form validation
    if not username:
        return render(request, 'orders/register.html', {"message": "No username."})
    elif len(username) < 4:
        return render(request, 'orders/register.html', {"message": "Username should be longer than 4 characters."})
    elif not email:
        return render(request, 'orders/register.html', {"message": "No Email."})
    # Email validation required.
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

    # Server-side form validation
    if not username:
        return render(request, 'orders/login.html', {"message": "No username."})
    elif len(username) < 4:
        return render(request, 'orders/login.html', {"message": "Username should be longer than 4 characters."})
    elif not password:
        return render(request, 'orders/login.html', {"message": "Type your password."})
    else:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'orders/login.html', {"message": "Login failed."})

def logout_view(request):
    logout(request)
    return render(request, 'orders/login.html', {"message": "Successfully logged out."})

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