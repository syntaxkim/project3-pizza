from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Review
from .forms import ReviewForm

# Create your views here.

# Load reviews with django paginator.
def review_list(request):
    # Load reviews with django paginator.
    reviews = get_list_or_404(Review)
    context = {"reviews": reviews}
    return render(request, 'reviews/review_list.html', context)

# Return a review
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    context = {"review": review}
    return render(request, 'reviews/review_detail.html', context)

def post_review(request):
    if request.method == 'GET':
        # Load post review form page.
        context = {"review_form": ReviewForm}
        return render(request, 'reviews/post_review.html', context)

    # Create a review
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            print(title)
            print(content)
            print(image)

        # review = Review(user=request.user, title=title, content=content, image=image)
        # review.save()

        return HttpResponseRedirect(reverse('review_list'))
        # return HttpResponseRedirect(reverse('review_detail', kwargs={'pk': review.id}))
