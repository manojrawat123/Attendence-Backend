from django.db import models

# Create your models here.
class EmailTemplate(models.Model):
    template_name = models.CharField(max_length=300 , unique=True)
    subject = models.CharField(max_length=300)
    template_body = models.TextField()
    signature = models.TextField() 
    display = models.BooleanField(default=False)
