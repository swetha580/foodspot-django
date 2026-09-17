from django.views.generic import ListView, DetailView
from app.models import Restaurant, Cuisine, Bookmark, Visited
from app.filters import RestaurantFilter


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'app/restaurant_list.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Restaurant.objects.all().order_by('name')
        self.filterset = RestaurantFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['cuisines'] = Cuisine.objects.all().order_by('name')

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_string'] = query_params.urlencode()

        context['spotlight_restaurants'] = Restaurant.objects.filter(is_spotlight=True).order_by('name')

        return context


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'app/restaurant_detail.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_bookmarked = False
        is_visited = False
        if self.request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.filter(
                user=self.request.user, restaurant=self.object
            ).exists()
            is_visited = Visited.objects.filter(
                user=self.request.user, restaurant=self.object
            ).exists()
        context['is_bookmarked'] = is_bookmarked
        context['is_visited'] = is_visited
        context['reviews'] = self.object.reviews.select_related('user').order_by('-created_at')[:5]
        context['review_count'] = self.object.reviews.count()
        return context
