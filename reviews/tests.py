from django.test import TestCase, Client
from django.db.models import Max

from .models import Review, User

# pylint: disable=no-member

# Create your tests here.
class ReviewsTestCase(TestCase):

    def setUp(self):

        # Create a user.
        user = User.objects.create(username='User', password='passw0rd')

        # Create reviews.
        Review.objects.create(user=user, title='review1', content='content1')
        Review.objects.create(user=user, title='review2', content='content2')

    ### View-side tests
    def test_index(self):
        c = Client()
        response = c.get("/reviews/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["review_list"].count(), 2)

    def test_valid_review_page(self):
        review_1 = Review.objects.get(title='review1')
        c = Client()
        response = c.get(f"/reviews/{review_1.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_review_page(self):
        max_id = Review.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        response = c.get(f"/reviews/{max_id + 1}")
        self.assertEqual(response.status_code, 404)