from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from app.forms import ReviewForm
from app.models import Restaurant, Review


class SubmitReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'app/submit_review.html'

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=kwargs['pk'])
        if request.user.is_authenticated and Review.objects.filter(user=request.user, restaurant=self.restaurant).exists():
            return redirect('restaurant_detail', pk=self.restaurant.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.restaurant
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = self.restaurant
        response = super().form_valid(form)
        self._update_average_rating()
        return response

    def _update_average_rating(self):
        avg = self.restaurant.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        self.restaurant.average_rating = round(avg, 2)
        self.restaurant.save(update_fields=['average_rating'])

    def get_success_url(self):
        return reverse('restaurant_detail', kwargs={'pk': self.restaurant.pk})
