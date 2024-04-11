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
from django.core.mail import EmailMessage
from datetime import datetime, timedelta


class GetLeaveApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        try:
            date = request.data.get("date")
            toDate = request.data.get("toDate")
            employee_user = request.user
            if date == toDate:
                my_leave_serializer = MyLeaveSerializer(data={
                    "date" : date,
                    "employee_user" : employee_user.id
                })
                if my_leave_serializer.is_valid():
                    my_leave_serializer.save()
                    email = EmailMessage(f"{employee_user.name} Applied for a leave","Leave Applied for {date}",'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com"])
                    email.send()
                    return Response({"message" : "Leave Granted Successfully"})
                else:
                    return Response(my_leave_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif date < toDate:
                one_day = timedelta(days = 1)
                start_date = datetime.strptime('2024-04-11', '%Y-%m-%d')
                end_date = datetime.strptime('2024-06-11', '%Y-%m-%d')
                
                current_date = start_date
                while(current_date <= end_date):
                    current_date += one_day
                    err_date_arr = []
                    my_leave_serializer = MyLeaveSerializer(data={
                    "date" : current_date.strftime('%Y-%m-%d'),
                    "employee_user" : employee_user.id
                })                
                    if my_leave_serializer.is_valid():
                        my_leave_serializer.save()
                    else:
                        err_date_arr = err_date_arr.append(current_date)
                    if(current_date == end_date):
                        print(err_date_arr)
                        return Response({"message" : "Leave Applied Successfully"})
                print({
                    "date" : date,
                    "To Date" : toDate
                })
                return Response({"message" : "Leave Granted Successfully"})

        except IntegrityError as e:
            return Response({"error": "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal server error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)