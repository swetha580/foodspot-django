from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Restaurant, Review


class SubmitReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant', city='Test City', address='123 Test St',
            timings='9am-9pm', cost_for_two=500, veg_type='veg',
        )

    def test_requires_login(self):
        response = self.client.get(reverse('submit_review', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_submit_review_creates_review(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('submit_review', args=[self.restaurant.pk]), {
            'rating': 4,
            'comment': 'Great food!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, restaurant=self.restaurant, rating=4).exists())

    def test_average_rating_recalculated(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('submit_review', args=[self.restaurant.pk]), {
            'rating': 5,
            'comment': 'Excellent!',
        })
        self.restaurant.refresh_from_db()
        self.assertEqual(float(self.restaurant.average_rating), 5.0)

    def test_duplicate_review_redirects(self):
        self.client.login(username='testuser', password='testpass123')
        Review.objects.create(user=self.user, restaurant=self.restaurant, rating=3, comment='ok')
        response = self.client.get(reverse('submit_review', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('restaurant_detail', args=[self.restaurant.pk]), response.url)
