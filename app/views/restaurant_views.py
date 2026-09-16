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
        context['cities'] = Restaurant.objects.values_list('city', flat=True).distinct().order_by('city')
        context['cuisines'] = Cuisine.objects.all().order_by('name')
        context['selected_city'] = self.request.GET.get('city', '')
        context['selected_cuisine'] = self.request.GET.get('cuisine', '')
        context['selected_veg_type'] = self.request.GET.get('veg_type', '')
        context['selected_is_open'] = self.request.GET.get('is_open', '')
        context['min_cost'] = self.request.GET.get('min_cost', '')
        context['max_cost'] = self.request.GET.get('max_cost', '')
        return context

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'app/restaurant_detail.html'
    context_object_name = 'restaurant'
