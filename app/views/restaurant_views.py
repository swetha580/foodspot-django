from django.views.generic import ListView
from app.models import Restaurant


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'app/restaurant_list.html'
    paginate_by = 9
    queryset = Restaurant.objects.all().order_by('name')
