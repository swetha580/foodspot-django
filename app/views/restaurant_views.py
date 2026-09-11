from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from app.models import Restaurant


def restaurant_list(request):
    restaurants = Restaurant.objects.all().order_by('name')
    paginator = Paginator(restaurants, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/restaurant_list.html', {'page_obj': page_obj})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'app/restaurant_detail.html', {'restaurant': restaurant})
