from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from app.models import Restaurant, Bookmark


class ToggleBookmarkView(LoginRequiredMixin, View):
    def post(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, restaurant=restaurant)
        if not created:
            bookmark.delete()
        return redirect(request.META.get('HTTP_REFERER', 'restaurant_list'))
