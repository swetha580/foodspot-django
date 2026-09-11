from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from app.models import Restaurant, Bookmark


@login_required
@require_POST
def toggle_bookmark(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, restaurant=restaurant)
    if not created:
        bookmark.delete()
    return redirect(request.META.get('HTTP_REFERER', 'restaurant_list'))
