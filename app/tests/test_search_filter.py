from django.test import TestCase
from django.urls import reverse

from app.models import Restaurant


class RestaurantSearchFilterTests(TestCase):
    def setUp(self):
        Restaurant.objects.create(
            name='Spice Garden', city='Madurai', address='1 Test St',
            timings='9-9', cost_for_two=300, veg_type='veg',
        )
        Restaurant.objects.create(
            name='Ocean Grill', city='Madurai', address='2 Test St',
            timings='9-9', cost_for_two=400, veg_type='non_veg',
        )

    def test_search_matches_partial_name(self):
        response = self.client.get(reverse('restaurant_list'), {'name': 'spice'})
        self.assertContains(response, 'Spice Garden')
        self.assertNotContains(response, 'Ocean Grill')

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse('restaurant_list'), {'name': ''})
        self.assertContains(response, 'Spice Garden')
        self.assertContains(response, 'Ocean Grill')
