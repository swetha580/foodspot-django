from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
        self.restaurant.update_average_rating()
        return response

    def get_success_url(self):
        return reverse('restaurant_detail', kwargs={'pk': self.restaurant.pk})


class ReviewListView(ListView):
    model = Review
    template_name = 'app/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Review.objects.filter(restaurant=self.restaurant).select_related('user').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.restaurant
        return context


class EditReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'app/edit_review.html'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.restaurant.update_average_rating()
        return response

    def get_success_url(self):
        return reverse('restaurant_detail', kwargs={'pk': self.object.restaurant.pk})


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        restaurant = self.object.restaurant
        response = super().post(request, *args, **kwargs)
        restaurant.update_average_rating()
        return response

    def get_success_url(self):
        return reverse('restaurant_detail', kwargs={'pk': self.object.restaurant.pk})
