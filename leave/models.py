from django.db import models
from employee.models import EmployeeUser

# Create your models here.
class Leave(models.Model):
    employee_user = models.ForeignKey(EmployeeUser, on_delete = models.CASCADE)
    date = models.DateField()
    class Meta:
        unique_together = ('employee_user', 'date')
    