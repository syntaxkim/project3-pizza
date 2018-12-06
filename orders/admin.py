from django.contrib import admin

from orders.models import Category, Pizza, Topping, Sub, Extra, Pasta, Salad, Dinner, CartItem, OrderItem, Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ("items",)
    list_display = ('order_time', 'user', 'contact', 'subtotal', 'recieved')
    list_filter = ['order_time', 'status', 'recieved']
    search_fields = ['user', 'contact', 'message', 'billing_address', 'shipping_address']

class ToppingAdmin(admin.ModelAdmin):
    filter_horizontal = ("toppings",)

# Category
admin.site.register(Category)

# Menu
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Extra)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner)

# Cart
admin.site.register(CartItem, ToppingAdmin)

# Order
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, ToppingAdmin)