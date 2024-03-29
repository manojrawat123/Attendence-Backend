from django.db import models

# Create your models here.
class Branch(models.Model):
    branch_name = models.CharField(max_length = 225)
    location = models.CharField(max_length = 225)
    branch_email = models.EmailField()
    service = models.CharField(max_length=225)

    def __str__(self):
        return self.branch_name