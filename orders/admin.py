from django.contrib import admin
from orders.models import Category, Pizza, Topping, Sub, Pasta, Salad, Dinner

# Register your models here.
admin.site.register(Category)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner)