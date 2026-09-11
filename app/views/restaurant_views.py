from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from app.models import Restaurant, Cuisine


def restaurant_list(request):
    restaurants = Restaurant.objects.all().order_by('name')

    city = request.GET.get('city')
    cuisine_id = request.GET.get('cuisine')
    veg_type = request.GET.get('veg_type')
    is_open = request.GET.get('is_open')
    min_cost = request.GET.get('min_cost')
    max_cost = request.GET.get('max_cost')

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

    restaurants = restaurants.distinct()

    paginator = Paginator(restaurants, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cities = Restaurant.objects.values_list('city', flat=True).distinct().order_by('city')
    cuisines = Cuisine.objects.all().order_by('name')

    context = {
        'page_obj': page_obj,
        'cities': cities,
        'cuisines': cuisines,
        'selected_city': city or '',
        'selected_cuisine': cuisine_id or '',
        'selected_veg_type': veg_type or '',
        'selected_is_open': is_open or '',
        'min_cost': min_cost or '',
        'max_cost': max_cost or '',
    }
    return render(request, 'app/restaurant_list.html', context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'app/restaurant_detail.html', {'restaurant': restaurant})
