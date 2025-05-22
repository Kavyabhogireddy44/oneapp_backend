from django.db import models
from user.models import CustomUser

# Create your models here.
class Suggestion(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='suggestion', blank=True)
    subject=models.CharField(max_length=200)
    suggesion=models.CharField(max_length=200)
    user_name=models.CharField(max_length=200, blank=True)
    created_time=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,default='sent', blank=True)

    def __str__(self):
        return self.subject


