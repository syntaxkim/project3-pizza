from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('item/<int:pk>', login_required(views.ItemDetail.as_view(), login_url='/login'), name='item_detail'),
    path('cart', login_required(views.CartItemList.as_view(), login_url='/login'), name='cart'),
    path('cart/add/<int:pk>', views.add_item, name='add_item'),
    path('cart/delete/<int:pk>', views.delete_item, name='delete_item'),
    path('order/orderStepFirst', views.order_first, name='order_first'),
    path('order/orderConfirm', views.order_confirm, name='order_confirm'),
    path('order/placeOrder', views.place_order, name='place_order'),
    path('order/result', views.order_result, name='order_result'),
    path('user/order', views.order_list, name='order_list'),
    path('user/order/<int:pk>', views.order_detail, name='order_detail'),
    path('manage/order', views.manage_order, name='manage_order'),
    path('manage/order/<int:pk>', views.manage_order_detail, name='manage_order_detail'),
]

# urlpatterns for function-based views
"""
urlpatterns_FBV = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('item/<int:item_id>', views.item, name='item_detail'),
    path('cart', views.cart_list, name='cart'),
    path('cart/add/<int:item_id>', views.add_item, name='add_item'),
    path('cart/delete/<int:item_id>', views.delete_item, name='delete_item'),
    path('order/orderStepFirst', views.order_first, name='order_first'),
    path('order/orderConfirm', views.order_confirm, name='order_confirm'),
    path('order/placeOrder', views.place_order, name='place_order'),
    path('order/result', views.order_result, name='order_result'),
    path('user/order', views.order_list, name='order_list'),
    path('user/order/<int:order_id>', views.order_detail, name='order_detail'),
    path('manage/order', views.manage_order, name='manage_order'),
    path('manage/order/<int:order_id>', views.manage_order_detail, name='manage_order_detail'),
]
"""