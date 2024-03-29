from employee.serializers import MyEmployeeSerializer, MyUserLoginSerializer,EmployeeRegisterSerializer
from employee.models import EmployeeUser 
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employee.renders import UserRenderer



# Create your views here.
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def EmailVerifyFunc(current_user, domain_name):
    try:
        mail_subject = "Please activate account"
        userid_encode = urlsafe_base64_encode(force_bytes(current_user.pk))
        token = default_token_generator.make_token(current_user)
        message = f'{domain_name}/accounts/activate/{userid_encode}/{token}'
        user_email = current_user.email
        email = EmailMessage(mail_subject, message, 'simply2cloud@gmail.com',[user_email])
        email.send()
    except Exception as e:
        print(e)


# Create your views here.
class CreateEmployeeUserView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        try:
            serializer = EmployeeRegisterSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
                user = EmployeeUser.objects.get(email= request.data.get("email"))
                user.is_active = True
                user.save()
                return Response({"message": "Registration Successfully Verify link Send to Your Email"})
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MyEmployeeLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        try:
            serializers = MyUserLoginSerializer(data=request.data)
            if serializers.is_valid(raise_exception=True):
                email = serializers.data.get("email")
                password = serializers.data.get("password")
                user = authenticate(email = email, password = password)
                user_serializer = MyEmployeeSerializer(user)
                if user is not None:
                    token = get_token_for_user(user)
                    return Response({'token': token, 'msg': "User Login Sucessfully" , "user_id" : user.id, "user" :{**user_serializer.data,"id" : user.id, "is_superuser":user.is_superuser}}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : "Invalid Info"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckEmailApi(APIView):
    def post(self, request, format=None):
        try: 
            email = request.data.get("email")
            if email:
                if EmployeeUser.objects.filter(email=email).exists():
                    return Response({"error" : "Email Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message" : "Email can used "}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : "Please provide email address"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetUserInfoAdmin(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format = None):
        try:
            employee_list = EmployeeUser.objects.all()
            employee_serializer = MyEmployeeSerializer(employee_list, many=True)
            return Response(employee_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)