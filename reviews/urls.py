from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewList.as_view(), name='review_list'),
    path('<int:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('post', login_required(views.PostReview.as_view(), login_url='/login'), name='post_review'),
    path('delete/<int:pk>', login_required(views.DeleteReview.as_view(), login_url='/login'), name='delete_review'),
]