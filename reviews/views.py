from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import ReviewForm

# Create your views here.
def index(request):
    # Load reviews with django paginator.

    return render(request, 'reviews/index.html')

def post_review(request):
    if request.method == 'GET':
        # Load post review form page.
        context = dict()
        context['review_form'] = ReviewForm
        return render(request, 'reviews/post_review.html', context)

    if request.method == 'POST':
        # Create review and redirect review index page
        return HttpResponseRedirect(reverse('index'))
