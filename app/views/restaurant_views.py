from django.views.generic import ListView, DetailView
from app.models import Restaurant


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'app/restaurant_list.html'
    paginate_by = 9
    queryset = Restaurant.objects.all().order_by('name')


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'app/restaurant_detail.html'
    context_object_name = 'restaurant'
