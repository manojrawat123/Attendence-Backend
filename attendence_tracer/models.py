from django.db import models
from employee.models import EmployeeUser

# Create your models here.
class Attendence(models.Model):
    employee_user = models.ForeignKey(EmployeeUser, on_delete = models.CASCADE)
    check_in_time = models.TimeField(auto_now_add=True)
    check_out_time = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('employee_user', 'date')