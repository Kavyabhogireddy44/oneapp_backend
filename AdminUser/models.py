from django.db import models

# Create your models here.
class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_image = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True,unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=[
        ('vender', 'Vender'),
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('verifier', 'Verifier'),
        ('manager', 'Manager'),
        ('support', 'Support'),
        ('auditor', 'Auditor'),
        ('analyst', 'Analyst'),
        ('moderator', 'Moderator'),
        ('guest', 'Guest'),
    ], default='user')
    password_field = models.CharField(max_length=138)  # Store hashed password

    def __str__(self):
        return self.phone
