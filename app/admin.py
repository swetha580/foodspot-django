from django.contrib import admin
from app.models import (
    Restaurant, Cuisine, MenuItem, RestaurantPhoto, Bookmark, Visited, Review
)

admin.site.register(Restaurant)
admin.site.register(Cuisine)
admin.site.register(MenuItem)
admin.site.register(RestaurantPhoto)
admin.site.register(Bookmark)
admin.site.register(Visited)
admin.site.register(Review)
