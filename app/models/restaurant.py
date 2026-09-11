from django.db import models

class Restaurant(models.Model):
    VEG_CHOICES = [
        ('veg', 'Veg'),
        ('non_veg', 'Non-Veg'),
        ('vegan', 'Vegan'),
    ]

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    timings = models.CharField(max_length=255)
    cost_for_two = models.PositiveIntegerField()
    veg_type = models.CharField(max_length=10, choices=VEG_CHOICES)
    is_open = models.BooleanField(default=True)
    is_spotlight = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    cuisines = models.ManyToManyField('app.Cuisine', related_name='restaurants', blank=True)

    def __str__(self):
        return self.name
