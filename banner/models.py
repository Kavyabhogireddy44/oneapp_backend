from django.db import models

class Banner(models.Model):
    img = models.URLField()
    route = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
