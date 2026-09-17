from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, ListView
from app.models import Restaurant, Visited


class ToggleVisitedView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=kwargs['pk'])
        visited, created = Visited.objects.get_or_create(user=self.request.user, restaurant=restaurant)
        if not created:
            visited.delete()
        return self.request.META.get('HTTP_REFERER', '/')


class VisitedListView(LoginRequiredMixin, ListView):
    model = Visited
    template_name = 'app/visited_list.html'
    context_object_name = 'visited_items'
    paginate_by = 9

    def get_queryset(self):
        return Visited.objects.filter(user=self.request.user).select_related('restaurant').order_by('-created_at')
