from django.db import models

# Create your models here.
class SharedSlides(models.Model):
    share_code=models.CharField(max_length=12,unique=True)
    slides_json = models.JSONField()
    created_at=models.DateTimeField(auto_now_add=True)