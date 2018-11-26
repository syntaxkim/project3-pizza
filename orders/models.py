from django.db import models

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
    PASTA = 'Pasta'
    SALAD = 'Salad'
    DINNER = 'Dinner Platters'
    CATEGORY_CHOICES = (
        (PIZZA, 'Pizza'),
        (TOPPING, 'Topping'),
        (SUB, 'Sub menu'),
        (PASTA, 'Pasta'),
        (SALAD, 'Salad'),
        (DINNER, 'Dinner Platters')
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
    price = models.IntegerField(blank=True, default=0) # Blankable for Toppings

    def __str__(self):
        return f"{self.category}: {self.name} _ {self.price}"

class Pizza(Item):
    """Define pizzas."""
    REGULAR = 'Regular'
    SICILIAN = 'Sicilian'
    CRUST_CHOICES = (
        (REGULAR, 'Regular'),
        (SICILIAN, 'Sicilian')
    )
    crust = models.CharField(max_length=8, choices=CRUST_CHOICES)
    S = 'Small'
    L = 'Large'
    SIZE_CHOICES = (
        (S, 'Small'),
        (L, 'Large')
    )
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)
    max_toppings = models.IntegerField(default=0)
    toppings = models.ManyToManyField('Topping', blank=True, related_name='toppings')

    def __str__(self):
        return f"{self.crust} Pizza with {self.name} ({self.size}) _ {self.price}"

class Topping(Item):
    """Define toppings."""
    def __str__(self):
        return f"{self.name}"

class Sub(Item):
    """Define sub-menus."""
    S = 'Small'
    L = 'Large'
    SIZE_CHOICES = (
        (S, 'Small'),
        (L, 'Large')
    )
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.size}) _ {self.price}"

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
    S = 'Small'
    L = 'Large'
    SIZE_CHOICES = (
        (S, 'Small'),
        (L, 'Large')
    )
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)

    class Meta:
        verbose_name = "Dinner Platter"
        verbose_name_plural = "Dinner Platters"

    def __str__(self):
        return f"{self.name} ({self.size}) _ {self.price}"
