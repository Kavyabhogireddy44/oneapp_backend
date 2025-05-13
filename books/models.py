from django.db import models
from django.contrib.postgres.fields import ArrayField

class Service(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('coming_soon', 'Coming Soon'),
        ('not_available', 'Not Available'),
    ]

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    img = models.URLField()
    offers = models.CharField(max_length=50)
    width = models.CharField(max_length=10)
    route = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    # city = models.CharField(max_length=100)
    city = ArrayField(models.CharField(max_length=100),blank=True,default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title
