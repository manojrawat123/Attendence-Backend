from django.db import models
from batch.models import BatchModel
from employee.models import EmployeeUser

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=200)
    batch_id = models.ForeignKey(BatchModel, on_delete=models.CASCADE)
    student_phone = models.IntegerField()
    student_email = models.EmailField()
    added_by = models.ForeignKey(EmployeeUser, on_delete=models.CASCADE, related_name = "student_added_by")
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=200, choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])