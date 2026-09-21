from django.test import TestCase
from django.urls import reverse

from app.models import Restaurant


class SpotlightListViewTests(TestCase):
    def setUp(self):
        Restaurant.objects.create(
            name='Spotlight Place', city='Test City', address='1 Test St',
            timings='9-9', cost_for_two=300, veg_type='veg', is_spotlight=True,
        )
        Restaurant.objects.create(
            name='Regular Place', city='Test City', address='2 Test St',
            timings='9-9', cost_for_two=300, veg_type='veg', is_spotlight=False,
        )

    def test_only_shows_spotlight_restaurants(self):
        response = self.client.get(reverse('spotlight_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spotlight Place')
        self.assertNotContains(response, 'Regular Place')
