from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Restaurant, Review


class EditDeleteReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='testpass123')
        self.other_user = User.objects.create_user(username='intruder', password='testpass123')
        self.restaurant = Restaurant.objects.create(
            name='Edit Test Restaurant', city='Test City', address='123 Test St',
            timings='9am-9pm', cost_for_two=500, veg_type='veg',
        )
        self.review = Review.objects.create(
            user=self.user, restaurant=self.restaurant, rating=3, comment='Okay food'
        )

    def test_owner_can_edit_review(self):
        self.client.login(username='owner', password='testpass123')
        response = self.client.post(reverse('edit_review', args=[self.review.pk]), {
            'rating': 5, 'comment': 'Actually great!'
        })
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Actually great!')

    def test_average_rating_updates_after_edit(self):
        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('edit_review', args=[self.review.pk]), {
            'rating': 5, 'comment': 'Updated'
        })
        self.restaurant.refresh_from_db()
        self.assertEqual(float(self.restaurant.average_rating), 5.0)

    def test_non_owner_cannot_edit_review(self):
        self.client.login(username='intruder', password='testpass123')
        response = self.client.get(reverse('edit_review', args=[self.review.pk]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_review(self):
        self.client.login(username='owner', password='testpass123')
        response = self.client.post(reverse('delete_review', args=[self.review.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_non_owner_cannot_delete_review(self):
        self.client.login(username='intruder', password='testpass123')
        response = self.client.post(reverse('delete_review', args=[self.review.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())

    def test_average_rating_updates_after_delete(self):
        Review.objects.create(user=self.other_user, restaurant=self.restaurant, rating=5, comment='Loved it')
        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('delete_review', args=[self.review.pk]))
        self.restaurant.refresh_from_db()
        self.assertEqual(float(self.restaurant.average_rating), 5.0)
