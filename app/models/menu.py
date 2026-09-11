from django.db import models

class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        'app.Restaurant', on_delete=models.CASCADE, related_name='menu_items'
    )
    dish_name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dish_name} - {self.restaurant.name}"
