from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Polygon(models.Model):
    center = models.JSONField()
    polygon = models.JSONField(null=True, blank=True)
    inside_color = models.CharField()
    border_color = models.CharField()

    def __str__(self):
        return f"AreaPolygon {self.id} - Center: {self.center}, Polygon: {self.polygon}"
