from django.db import models
from employee.models import EmployeeUser

# Create your models here.
class Leave(models.Model):
    employee_user = models.ForeignKey(EmployeeUser, on_delete = models.CASCADE)
    date = models.DateField()
#     leave_type = models.CharField(choices=[
#         ('half_day', 'Half Day'),
#         ('full_day', 'Full Day'),
#         ('custom', 'Custom'),
#     ], null=True, blank=True
# )
    class Meta:
        unique_together = ('employee_user', 'date')
    