from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('item/<int:item_id>', views.item, name='item_detail'),
    path('cart', views.index, name='cart'),
    path('cart/add/<int:item_id>', views.add_item, name="add_item"),
    path('cart/delete/<int:item_id>', views.delete_item, name="delete_item"),
]