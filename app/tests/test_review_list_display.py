from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Restaurant, Review


class ReviewListDisplayTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reviewer', password='testpass123')
        self.restaurant = Restaurant.objects.create(
            name='Review Test Restaurant', city='Test City', address='123 Test St',
            timings='9am-9pm', cost_for_two=500, veg_type='veg',
        )

    def test_detail_page_shows_review_preview(self):
        Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4, comment='Nice place!')
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.pk]))
        self.assertContains(response, 'reviewer')
        self.assertContains(response, 'Nice place!')
        self.assertContains(response, '★★★★☆')

    def test_detail_page_empty_reviews_state(self):
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.pk]))
        self.assertContains(response, 'No reviews yet')

    def test_detail_page_shows_see_all_link_when_more_than_5(self):
        other_restaurant = self.restaurant
        for i in range(6):
            u = User.objects.create_user(username=f'user{i}', password='pass12345')
            Review.objects.create(user=u, restaurant=other_restaurant, rating=3, comment=f'Review {i}')
        response = self.client.get(reverse('restaurant_detail', args=[other_restaurant.pk]))
        self.assertContains(response, 'See all 6 reviews')


class ReviewListViewTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Paginated Restaurant', city='Test City', address='123 Test St',
            timings='9am-9pm', cost_for_two=500, veg_type='veg',
        )
        self.other_restaurant = Restaurant.objects.create(
            name='Other Restaurant', city='Test City', address='456 Test St',
            timings='9am-9pm', cost_for_two=500, veg_type='veg',
        )
        for i in range(12):
            u = User.objects.create_user(username=f'reviewer{i}', password='pass12345')
            Review.objects.create(user=u, restaurant=self.restaurant, rating=(i % 5) + 1, comment=f'Comment {i}')
        u2 = User.objects.create_user(username='otherreviewer', password='pass12345')
        Review.objects.create(user=u2, restaurant=self.other_restaurant, rating=5, comment='Other restaurant review')

    def test_pagination_shows_10_per_page(self):
        response = self.client.get(reverse('review_list', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reviews']), 10)

    def test_second_page_shows_remaining(self):
        response = self.client.get(reverse('review_list', args=[self.restaurant.pk]) + '?page=2')
        self.assertEqual(len(response.context['reviews']), 2)

    def test_only_shows_this_restaurant_reviews(self):
        response = self.client.get(reverse('review_list', args=[self.restaurant.pk]))
        self.assertNotContains(response, 'Other restaurant review')
