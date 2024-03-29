from leave.models import Leave
from rest_framework import serializers

class MyLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"