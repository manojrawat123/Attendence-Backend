from emailtemplate.models import EmailTemplate
from rest_framework import serializers

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = EmailTemplate