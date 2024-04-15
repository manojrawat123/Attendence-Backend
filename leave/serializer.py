from leave.models import Leave
from rest_framework import serializers
from datetime import date

class MyLeaveSerializer(serializers.ModelSerializer):
    is_editable = serializers.SerializerMethodField()
    class Meta:
        model = Leave
        fields = "__all__"

    def get_is_editable(self, obj):
        # Check if the leave date is in the future
        today = date.today()
        if obj.date > today:
            return True
        else:
            return False    
