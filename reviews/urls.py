from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewList.as_view(), name='review_list'),
    path('<int:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('post', views.PostReview.as_view(), name='post_review'),
]