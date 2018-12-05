from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewList.as_view(), name='review_list'),
    path('<int:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('post', views.post_review, name='post_review'),
]