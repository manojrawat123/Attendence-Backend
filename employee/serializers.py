from rest_framework import serializers 
from employee.models import EmployeeUser

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type" : "password"}, write_only=True)
    class Meta:
        model = EmployeeUser
        fields = ["email" , "name", "password", "password2"]
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password Didn't match")
        return attrs
    def create(self, validate_data):
        validate_data.pop("password2")
        return EmployeeUser.objects.create_user(**validate_data)
        
class MyEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ["name", "email", "id","address", "date_of_joining", "phone", "role" ]
        
class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ["password"]


class MyUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 225)
    class Meta:
        model = EmployeeUser
        fields = ["email", "password", "id"]

    def validate(self, data):
        for field_name, value in data.items():
            if value == "":
                raise serializers.ValidationError(f"{field_name} field is required.")
        return data
