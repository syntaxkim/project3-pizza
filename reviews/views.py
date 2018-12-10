from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, View

from .models import Review
from .forms import ReviewForm

# Create your views here.

# pylint: disable=no-member

# Load reviews with django paginator.
class ReviewList(ListView):
    model = Review
    paginate_by = 10
    ordering = ['-time_created']

# Return a review
class ReviewDetail(DetailView):
    model = Review

class PostReview(View):
    # Load form page.
    def get(self, request, *args, **kwargs):
        context = {"review_form": ReviewForm}
        return render(request, 'reviews/post_review.html', context)

    # Create a review
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST, request.FILES or None)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']

            review = Review(user=request.user, title=title, content=content, image=image)
            review.save()

        return HttpResponseRedirect(reverse('review_detail', kwargs={'pk': review.id}))

class DeleteReview(DeleteView):
    model = Review
    success_url = reverse_lazy('review_list')
