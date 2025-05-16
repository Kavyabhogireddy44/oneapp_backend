from django.db import models
from user.models import CustomUser

class Favourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favourites')
    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=100, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.user.username}"
