import django_filters
from app.models import Restaurant

VEG_TYPE_CHOICES = Restaurant._meta.get_field('veg_type').choices
IS_OPEN_CHOICES = (
    ('open', 'Open'),
    ('closed', 'Closed'),
)


class RestaurantFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    cuisine = django_filters.NumberFilter(field_name='cuisines__id')
    veg_type = django_filters.ChoiceFilter(choices=VEG_TYPE_CHOICES)
    is_open = django_filters.ChoiceFilter(
        choices=IS_OPEN_CHOICES, method='filter_is_open'
    )
    min_cost = django_filters.NumberFilter(field_name='cost_for_two', lookup_expr='gte')
    max_cost = django_filters.NumberFilter(field_name='cost_for_two', lookup_expr='lte')

    class Meta:
        model = Restaurant
        fields = ['city', 'cuisine', 'veg_type', 'is_open', 'min_cost', 'max_cost']

    def filter_is_open(self, queryset, name, value):
        if value == 'open':
            return queryset.filter(is_open=True)
        elif value == 'closed':
            return queryset.filter(is_open=False)
        return queryset
