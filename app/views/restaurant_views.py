from django.views.generic import ListView, DetailView
from app.models import Restaurant, Cuisine
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

        return context


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'app/restaurant_detail.html'
    context_object_name = 'restaurant'
