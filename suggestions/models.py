from django.db import models
from user.models import CustomUser

# Create your models here.
class Suggestion(models.Model):
    user=models.foreignKey(CustomUser,on_delete=models.CASCADE,related_name='suggestion')
    subject=models.charField(max_length=200)
    suggesion=models.CharField(max_length=200)
    user_name=models.CharField(max_length=200)
    created_time=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200)

    def __str__(self):
        return self.subject


