from django.db import models

class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(
        'app.Restaurant', on_delete=models.CASCADE, related_name='photos'
    )
    image = models.ImageField(upload_to='restaurant_photos/')

    def __str__(self):
        return f"Photo of {self.restaurant.name}"
