from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
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
from leave.models import Leave


class GetLeaveApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            year = request.GET.get("year")
            employee_leave = Leave.objects.filter(Q(employee_user = request.user.id) & Q(date__year=year))
            employee_leave_serializer = MyLeaveSerializer(employee_leave, many=True)
            return Response(employee_leave_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                    email = EmailMessage(f"{employee_user.name} Applied for a leave",f"Leave Applied for {date}",'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com", "vikas.sharma@simply2cloud.com"])
                    email.send()
                    return Response({"message" : "Leave Granted Successfully"}, status=status.HTTP_200_OK)
                else:
                    if 'non_field_errors' in my_leave_serializer.errors and 'unique' in my_leave_serializer.errors['non_field_errors'][0].code:
                        return Response({"error" : "Leave For this date Is already Taken"}, status=status.HTTP_400_BAD_REQUEST)
                    return Response(my_leave_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif date < toDate:
                one_day = timedelta(days = 1)
                start_date = datetime.strptime(date, '%Y-%m-%d')
                end_date = datetime.strptime(toDate, '%Y-%m-%d')

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
                email = EmailMessage(f"{employee_user.name} Applied for a leave",f"Leave Applied form {date} to {toDate}",'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com", "vikas.sharma@simply2cloud.com"])
                email.send()
                return Response({"message" : "Leave Granted Successfully"})
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal server error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def delete(self, request, id = None):
        try:
            print("hii")
            if(id == None):
                print("method not allowed")
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                leave_data = Leave.objects.get(id = id)
                if leave_data.employee_user.id == request.user.id:
                    leave_data.delete()
                    return Response({"message" : "Leave Canceled"}, status=status.HTTP_200_OK)
                else:
                    print("not match")
                    print({
                        "id" : id,
                        "employee_user" : leave_data.employee_user.id 
                           })
                    return Response({"message" : "Bad Request"} , status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)