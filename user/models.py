from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
