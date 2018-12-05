from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, DeleteView

from .models import Review
from .forms import ReviewForm

# Create your views here.

# pylint: disable=no-member

# Load reviews with django paginator.
class ReviewList(ListView):
    model = Review
    paginate_by = 5
    ordering = ['-time_created']

# Return a review
class ReviewDetail(DetailView):
    model = Review

def post_review(request):
    if request.method == 'GET':
        # Load form page.
        context = {"review_form": ReviewForm}
        return render(request, 'reviews/post_review.html', context)

    # Create a review
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']

            review = Review(user=request.user, title=title, content=content, image=image)
            review.save()

        return HttpResponseRedirect(reverse('review_detail', kwargs={'pk': review.id}))
