from django.db import models
from batch.models import BatchModel
from emailtemplate.models import EmailTemplate

class StudentMailer(models.Model):
    batch_id = models.ForeignKey(BatchModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    signature = models.TextField()
    def __str__(self):
        return self.subject
