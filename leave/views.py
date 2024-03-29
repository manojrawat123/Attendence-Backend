from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from leave.serializer import MyLeaveSerializer
from leave.models import Leave


class GetLeaveApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        try:
            date = request.data.get("date")
            print(date)
            employee_user = request.user.id
            my_leave_serializer = MyLeaveSerializer(data={
                "date" : date,
                "employee_user" : employee_user
            })
            if my_leave_serializer.is_valid():
                my_leave_serializer.save()
                return Response({"message" : "Leave Granted Successfully"})
            else:
                return Response(my_leave_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal server error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)