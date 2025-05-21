from django.db import models

from django.db import models
from user.models import CustomUser

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    token=models.CharField(max_length=200)
    service_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    service_image = models.URLField(max_length=500, blank=True, null=True)
    provider_id = models.CharField(max_length=50)
    provider_name = models.CharField(max_length=255)
    scheduled_date = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(auto_now_add=True)
    address = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('scheduled', 'Scheduled'),
            ('in-progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.service_name} for {self.user.username}"
