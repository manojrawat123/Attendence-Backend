from django.db import models
from student.models import Student
from batch.models import BatchModel


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  
    batch_id = models.ForeignKey(BatchModel, on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=50, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
        ('Holiday', 'Holiday'),
    ])
    
    class Meta:
        unique_together = (('student', 'date'),)