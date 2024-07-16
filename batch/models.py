from django.db import models
from employee.models import EmployeeUser
from mybrand.models import Brand 

# Create your models here.
class BatchModel(models.Model):
    batch_name = models.CharField(max_length=200)
    batch_start_timing = models.TimeField()
    batch_end_timing = models.TimeField()
    batch_days = models.JSONField()
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(EmployeeUser, on_delete= models.CASCADE, related_name="batch_created_by")
    assigned_to = models.ForeignKey(EmployeeUser, on_delete=models.CASCADE, related_name="batch_assigned_by")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)