from rest_framework import serializers
from studentattendence.models import Attendance

class StudentAttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"