from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Restaurant, Bookmark


class BookmarkToggleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            city='Test City',
            address='123 Test St',
            timings='9am-9pm',
            cost_for_two=500,
            veg_type='veg',
        )

    def test_bookmark_requires_login(self):
        response = self.client.post(reverse('toggle_bookmark', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_bookmark_toggle_creates_and_removes(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('toggle_bookmark', args=[self.restaurant.pk]))
        self.assertTrue(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())

        self.client.post(reverse('toggle_bookmark', args=[self.restaurant.pk]))
        self.assertFalse(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_bookmark_requires_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('toggle_bookmark', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 405)
