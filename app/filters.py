import django_filters
from app.models import Restaurant, Cuisine


class RestaurantFilter(django_filters.FilterSet):
    city = django_filters.ChoiceFilter(choices=[])
    cuisine = django_filters.ModelChoiceFilter(queryset=Cuisine.objects.all().order_by('name'))
    veg_type = django_filters.ChoiceFilter(choices=Restaurant._meta.get_field('veg_type').choices)
    is_open = django_filters.ChoiceFilter(
        choices=(('open', 'Open'), ('closed', 'Closed')),
        method='filter_is_open'
    )
    min_cost = django_filters.NumberFilter(field_name='cost_for_two', lookup_expr='gte')
    max_cost = django_filters.NumberFilter(field_name='cost_for_two', lookup_expr='lte')

    class Meta:
        model = Restaurant
        fields = ['city', 'cuisine', 'veg_type', 'is_open', 'min_cost', 'max_cost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cities = Restaurant.objects.values_list('city', flat=True).distinct().order_by('city')
        self.filters['city'].extra['choices'] = [(city, city) for city in cities]

    def filter_is_open(self, queryset, name, value):
        if value == 'open':
            return queryset.filter(is_open=True)
        elif value == 'closed':
            return queryset.filter(is_open=False)
        return queryset
