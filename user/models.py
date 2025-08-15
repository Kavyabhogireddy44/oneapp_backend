from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    fcm_token = models.CharField(max_length=255, blank=True)
    profile_image = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login= models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=50, choices=[
        ('user', 'User'),
        ('provider', 'Service Provider'),
        ('admin', 'Admin')
    ], default='user')

    def __str__(self):
        return self.username
