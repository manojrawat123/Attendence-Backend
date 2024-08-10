from studentmailer.models import StudentMailer
from rest_framework import serializers


class StudentMailerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = StudentMailer