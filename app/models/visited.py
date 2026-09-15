from django.conf import settings
from django.db import models
from .base import TimestampedModel


class Visited(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('app.Restaurant', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user} visited {self.restaurant}"
