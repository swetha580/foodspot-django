from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from app.models import Restaurant, Bookmark


class ToggleBookmarkView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=kwargs['pk'])
        bookmark, created = Bookmark.objects.get_or_create(user=self.request.user, restaurant=restaurant)
        if not created:
            bookmark.delete()
        return self.request.META.get('HTTP_REFERER', '/')
