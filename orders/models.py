from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    """Define Categories."""
    # Though you can define a choices list outside of a model class and then refer to it,
    # defining the choices and names for each choice inside the model class
    # keeps all of that information with the class that uses it,
    # and makes the choices easy to reference
    PIZZA = 'Pizza'
    TOPPING = 'Topping'
    SUB = 'Sub'
    EXTRA = 'Extra'
    PASTA = 'Pasta'
    SALAD = 'Salad'
    DINNER = 'Dinner Platter'
    CATEGORY_CHOICES = (
        (PIZZA, 'Pizza'),
        (TOPPING, 'Topping'),
        (SUB, 'Sub menu'),
        (EXTRA, 'Extra'),
        (PASTA, 'Pasta'),
        (SALAD, 'Salad'),
        (DINNER, 'Dinner Platter')
    )
    # In order to make custom categories, delete choices attribute.
    name = models.CharField(max_length=16, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

# Base model
class Item(models.Model):
    """Overall Item-Price table"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    S = 'Small'
    L = 'Large'
    SIZE_CHOICES = (
        (S, 'Small'),
        (L, 'Large')
    )
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, blank=True)
    price = models.IntegerField(blank=True, default=0) # Blankable for Toppings

    def __str__(self):
        return f"{self.category}: {self.name} _ {self.price}"

    def is_valid_item(self):
        return (self.price >= 0)

class Pizza(Item):
    """Define pizzas."""
    REGULAR = 'Regular'
    SICILIAN = 'Sicilian'
    CRUST_CHOICES = (
        (REGULAR, 'Regular'),
        (SICILIAN, 'Sicilian')
    )
    crust = models.CharField(max_length=8, choices=CRUST_CHOICES)
    max_toppings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.crust} Pizza with {self.name} ({self.size}) _ {self.price}"

class Topping(Item):
    """Define toppings."""
    def __str__(self):
        return f"{self.name}"

class Sub(Item):
    """Define sub-menus."""

    def __str__(self):
        return f"{self.name} ({self.size}) _ {self.price}"

class Extra(Item):
    """Define extra-options."""

    def __str__(self):
        return f"{self.name}"

class Pasta(Item):
    """Define pastas."""
    
    def __str__(self):
        return f"{self.name} _ {self.price}"

class Salad(Item):
    """Define salads."""
    
    def __str__(self):
        return f"{self.name} _ {self.price}"

class Dinner(Item):
    """Define dinner platters."""

    class Meta:
        verbose_name = "Dinner Platter"
        verbose_name_plural = "Dinner Platters"

    def __str__(self):
        return f"{self.name} ({self.size}) _ {self.price}"

class CartItem(models.Model):
    """Cart items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(Topping, blank=True, related_name='carts') # For pizza
    extra = models.BooleanField(default=False) # For sub
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} {self.item} {self.quantity}"

    def is_valid_cartitem(self):
        return (self.price > 0) and (self.quantity > 0)

class OrderItem(models.Model):
    """Order placed items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(Topping, blank=True, related_name='orders') # For pizza
    extra = models.BooleanField(default=False) # For sub
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} {self.item} {self.quantity}"

    def is_valid_orderitem(self):
        return (self.price > 0) and (self.quantity > 0)

class Order(models.Model):
    """Order summary""" # A set of order placed items
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    items = models.ManyToManyField(OrderItem, related_name='order')
    subtotal = models.IntegerField('Shipment Total', default=0)
    order_time = models.DateTimeField('Order placed', default=timezone.now)
    contact = models.CharField(max_length=100)
    billing_address = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=100)
    message = models.CharField(max_length=50, blank=True)
    ORDERED = 'Ordered'
    SHIPPING = 'On Shipping'
    DELIVERED = 'Delivered'
    STATUS_CHOCIES = (
        (ORDERED, 'Ordered'),
        (SHIPPING, 'On Shipping'),
        (DELIVERED, 'Delivered')
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOCIES, default=ORDERED)
    recieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.contact} {self.order_time} {self.status} {self.recieved}"

    def is_valid_order(self):
        return (self.subtotal > 0)