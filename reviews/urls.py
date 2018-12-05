from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reviews'),
    path('post', views.post_review, name='post_review'),
]