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
from attendence_tracer.models import Attendence
from datetime import date
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from employee.ForgotEmailSenderFunc import sendPasswordResetEmail

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
                user.date_of_birth = request.data.get('date_of_birth') if request.data.get('date_of_birth') is not None else None
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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            today = date.today()
            user = EmployeeUser.objects.get(id = request.user.id)
            user_serilaizer = MyEmployeeSerializer(user)
            try:
                attendence = Attendence.objects.get(employee_user = request.user.id, date=today)
                if attendence.check_in_time and attendence.check_out_time is None:
                    current_time = timezone.localtime(timezone.now()).time()
                    time_diff_seconds = (datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), attendence.check_in_time)).total_seconds()
                    show_checkout = True if time_diff_seconds > 14400 else False
                    return Response({"user_data" : user_serilaizer.data, "checkin_id" : attendence.id, "show_checkout_button" : show_checkout})
            except Exception as e:
                print(e)
            return Response({"user_data" : user_serilaizer.data})
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, id = None):
        try:
            if id is None and request.user.id != id:
                return Response({"error" : "Method Not Allowed"})
            else:
                user = EmployeeUser.objects.get(id = id)
                user_serializer = MyEmployeeSerializer(user, data=request.data, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({"message" : "Updated Successfully!"}, status=status.HTTP_200_OK)                
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
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

class ForgotPassword(APIView):
    def post(self , request, id = None):
        try:
            user = EmployeeUser.objects.get(Q(email = request.data.get("email")) & Q(is_active = True))
            domain_name = 'https://simply-2-cloud-attendence.vercel.app'
            if user is None:
                return Response({"error" : "Email Didn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                sendPasswordResetEmail(user, domain_name)
                return Response({"message" : "Reset Password Link Send to your email"},status=status.HTTP_200_OK)
        except Exception as e: 
            print(e)
            return Response({"error" : f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
class ResetPassword(APIView):
    def post(self , request, userid_encode = None,token = None):
        try:
            activate = request.data.get("activate")
            password = request.data.get('password')
            pk = urlsafe_base64_decode(userid_encode)
            print(pk)
            user = EmployeeUser.objects.get(pk= pk)
            if default_token_generator.check_token(user,token):
                print(password)
                h_password = make_password(password)
                print(h_password)
                serializer = MyEmployeeSerializer(user, data={"password" : h_password}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : "Not Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 


