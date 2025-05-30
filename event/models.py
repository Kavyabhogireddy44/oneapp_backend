from django.db import models
class Event(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.JSONField() 
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=list)
    organizer = models.CharField(max_length=200)
    contact = models.EmailField()
    isFree = models.BooleanField(default=True)
    ticketPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imageUrl = models.URLField(max_length=300)
    registrationUrl = models.URLField(max_length=300, null=True, blank=True)
    recurrence = models.CharField(max_length=50)
