from rest_framework import serializers
from batch.models import BatchModel

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchModel
        fields = "__all__"