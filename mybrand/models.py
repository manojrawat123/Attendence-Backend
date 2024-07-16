from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length = 225)
    location = models.CharField(max_length = 225)
    brand_email = models.EmailField()
    service = models.CharField(max_length=225)

    def __str__(self):
        return self.brand_name