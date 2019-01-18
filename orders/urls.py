from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.urls import path

from . import views

urlpatterns = [
    path('', views.RedirectView.as_view(url='/menu'), name='home'), # Redirect to menu
    path('menu', cache_page(3600 * 24, key_prefix="menu")(views.IndexView.as_view()), name='index'),
    path('item/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('cart', login_required(views.CartItemList.as_view(), login_url='/login'), name='cart'),
    path('cart/add/<int:pk>', login_required(views.AddItem.as_view(), login_url='/login'), name='add_item'),
    path('cart/delete/<int:pk>', login_required(views.DeleteItem.as_view(), login_url='/login'), name='delete_item'),
    path('order/orderStepFirst', views.order_first, name='order_first'), #FBV
    path('order/orderConfirm', views.order_confirm, name='order_confirm'), #FBV
    path('order/placeOrder', views.place_order, name='place_order'), #FBV
    path('order/result', views.order_result, name='order_result'), #FBV
    path('user/order', login_required(views.OrderList.as_view(), login_url='/login'), name='order_list'),
    path('user/order/<int:pk>', login_required(views.OrderDetail.as_view(), login_url='/login'), name='order_detail'),
    path('manage/order', views.ManageOrder.as_view(), name='manage_order'),
    path('manage/order/detail/<int:pk>', views.ManageOrderDetail.as_view(), name='manage_order_detail'),
    path('register', views.register, name='register'), #FBV
    path('login', views.login_view, name='login'), #FBV
    path('logout', views.logout_view, name='logout'), #FBV
]

# urlpatterns for function-based views only
"""
urlpatterns = [
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