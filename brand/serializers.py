from rest_framework import serializers
from brand.models import Branch

class MyBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"