from rest_framework import serializers
from attendence_tracer.models import Attendence


class MyAttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = "__all__"