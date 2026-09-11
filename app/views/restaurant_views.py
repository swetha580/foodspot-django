from django.views.generic import ListView, DetailView
from app.models import Restaurant, Cuisine


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'app/restaurant_list.html'
    paginate_by = 9

    def get_queryset(self):
        restaurants = Restaurant.objects.all().order_by('name')

        city = self.request.GET.get('city')
        cuisine_id = self.request.GET.get('cuisine')
        veg_type = self.request.GET.get('veg_type')
        is_open = self.request.GET.get('is_open')
        min_cost = self.request.GET.get('min_cost')
        max_cost = self.request.GET.get('max_cost')

        if city:
            restaurants = restaurants.filter(city__iexact=city)
        if cuisine_id:
            restaurants = restaurants.filter(cuisines__id=cuisine_id)
        if veg_type:
            restaurants = restaurants.filter(veg_type=veg_type)
        if is_open == 'open':
            restaurants = restaurants.filter(is_open=True)
        elif is_open == 'closed':
            restaurants = restaurants.filter(is_open=False)
        if min_cost:
            restaurants = restaurants.filter(cost_for_two__gte=min_cost)
        if max_cost:
            restaurants = restaurants.filter(cost_for_two__lte=max_cost)

        return restaurants.distinct()

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
