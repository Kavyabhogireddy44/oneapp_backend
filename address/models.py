from django.db import models
from user.models import CustomUser

# Create your models here.
class Address(models.Model):
    LABEL_CHOICES = [
        ('home','HOME'),
        ('work','WORK'),
        ('school','SCHOOL'),
        ('other','OTHER')
    ]
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='address')
    lat=models.CharField(max_length=200)
    lng=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    landmark=models.CharField(max_length=200)
    label=models.CharField(max_length=200,choices=LABEL_CHOICES)
    house_no=models.CharField(max_length=200)
    building_name=models.CharField(max_length=200)
    receiver_name=models.CharField(max_length=200)
    conatact=models.CharField(max_length=200)

    def __str__(self):
        return self.address
    
