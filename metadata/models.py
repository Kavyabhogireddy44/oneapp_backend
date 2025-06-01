from django.db import models

# Create your models here.
class MetaData(models.Model):
    latest_version = models.CharField(max_length=100, unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    download_link=models.CharField(max_length=255)
    video=models.CharField()
    

    def __str__(self):
        return f"{self.key}: {self.value}"

