from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('<int:pk>', views.review_detail, name='review_detail'),
    path('post', views.post_review, name='post_review'),
]