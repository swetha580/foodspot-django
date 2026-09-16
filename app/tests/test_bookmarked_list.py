from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Restaurant, Bookmark


class BookmarkedListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.restaurant1 = Restaurant.objects.create(
            name='Restaurant One', city='City A', address='Addr 1',
            timings='9-9', cost_for_two=300, veg_type='veg',
        )
        self.restaurant2 = Restaurant.objects.create(
            name='Restaurant Two', city='City B', address='Addr 2',
            timings='9-9', cost_for_two=400, veg_type='non_veg',
        )
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant1)
        Bookmark.objects.create(user=self.other_user, restaurant=self.restaurant2)

    def test_requires_login(self):
        response = self.client.get(reverse('bookmarked_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_shows_only_own_bookmarks(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookmarked_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restaurant One')
        self.assertNotContains(response, 'Restaurant Two')

    def test_empty_state(self):
        self.client.login(username='otheruser', password='testpass123')
        Bookmark.objects.filter(user=self.other_user).delete()
        response = self.client.get(reverse('bookmarked_list'))
        self.assertContains(response, "haven't bookmarked")
