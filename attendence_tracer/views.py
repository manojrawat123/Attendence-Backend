from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from attendence_tracer.serializer import MyAttendenceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from attendence_tracer.models import Attendence
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from django.db import IntegrityError
from leave.models import Leave
import calendar
from attendence_tracer.monthAttendence import attendance_data_func_month
from employee.models import EmployeeUser

def validateLocation(latitude, longitude):
    try:
        if longitude is None or latitude is None:
            return Response({"error" : "Longitude and latitude cannot be null"}, status=status.HTTP_400_BAD_REQUEST)
        specified_latitude = radians(28.7001186)
        specified_longitude = radians(77.1184777)
        # Provided location info
        provided_latitude = radians(latitude)
        provided_longitude = radians(longitude)
        # Calculate the distance between the provided location and the specified location
        dlon = provided_longitude - specified_longitude
        dlat = provided_latitude - specified_latitude
        a = sin(dlat / 2)**2 + cos(specified_latitude) * cos(provided_latitude) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371 * c * 1000  # Radius of the Earth in

        if distance > 100:
            email = EmailMessage("Checkin Failed", f"lattitude: {latitude}, longitude: {longitude}  {distance} meters", 'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com"])
            email.send()
            return False
        else:
            email = EmailMessage(f"{distance} meters", 'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com", "bahimunna457@gmail.com"])
            email.send()
            return distance
    except Exception as e:
        print(e)
        return Response({"error" : "Unable to get Location"}, status=status.HTTP_400_BAD_REQUEST)


def attendence_data_func_year(attendence_detail, leave_detail):
    attendance_data = {}
    for i in range(1, 13):
        month_name = calendar.month_name[i]
        attendance_data[month_name] = {"present": 0, "half_days": 0, "leave": 0}
    for i in leave_detail:
        month = i.date.strftime("%B")
        attendance_data[month]["leave"] += 1
    for i in attendence_detail:
        month = i.date.strftime("%B")
        if i.check_in_time and i.check_out_time:
            attendance_data[month]["present"] += 1
        elif i.check_in_time:
            attendance_data[month]["half_days"] += 1
    return attendance_data

# Create your views here.
class CheckInView(APIView):
    permission_classes = [IsAuthenticated]
    time = datetime.now().time()

    def get(self, request, id = None):
        if id is not None:
            if request.user.is_superuser or request.user.id == id:
                year = request.GET.get("year")
                attendence_detail = Attendence.objects.filter(Q(employee_user = id) & Q(date__year=year))
                leave_detail = Leave.objects.filter(Q(employee_user = id))
                attendance_data = attendence_data_func_year(attendence_detail, leave_detail)
                return Response(attendance_data, status = status.HTTP_200_OK)
            else:
                return Response({"message" : "You are not Authenticated"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            attendence_detail = Attendence.objects.filter(Q(employee_user = request.user.id))
            leave_detail = Leave.objects.filter(Q(employee_user = request.user.id))
            attendance_data = attendence_data_func_year(attendence_detail, leave_detail)
            return Response(attendance_data, status= status.HTTP_200_OK)

    def post(self, request, id = None):
        try:
            longitude = request.data.get('longitude')
            lattitude = request.data.get('latitude')
            time = datetime.now().time().strftime("%H:%M")
            is_valid = validateLocation(latitude=lattitude, longitude=longitude)
            if is_valid == False:
                email_1 = EmailMessage("CheckIn Failed", "Checkin Failed at {time} ", 'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com"])
                email_1.send()
                return Response({"error":"Invalid Location"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                attendence_serializer = MyAttendenceSerializer(data={
                "employee_user" : request.data.get("user")
                })
                if attendence_serializer.is_valid():
                    attendence = attendence_serializer.save()
                    try:
                        name = request.user.name
                        user_email = request.user.email
                        email_1 = EmailMessage(f"{name} ", f"Checkin Successfully at {time} Distance from the office -: {is_valid}meters", 'simply2cloud@gmail.com',["vikas.sharma@simply2cloud.com", "positive.mind.123456789@gmail.com"])
                        email_2 = EmailMessage("Successfully Checked In!!", f"You checkin at {time}", 'simply2cloud@gmail.com',[user_email])
                        email_1.send()
                        email_2.send()
                    except Exception as e:
                        print("email failed")
                        print(e)
                    return Response({"attendence_id" : attendence.id}, status=status.HTTP_200_OK)
                else:
                    if attendence_serializer.errors.get("non_field_errors"):
                        return Response({'error': "You have already checked in today"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(attendence_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": "You have already checked in today"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal server error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id = None):

        try:
            if id is None:
                return Response({"error" : "method not allowed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                today_date = datetime.now()
                time = today_date.time()
                date = today_date.date()
                user_attendence = Attendence.objects.filter(employee_user = request.user.id)
                attendence = user_attendence.get(id = id)
                longitude = request.data.get('longitude')
                lattitude = request.data.get('latitude')
                print({"lattitude" : lattitude,
                    "longitude" : longitude})
                is_valid = validateLocation(latitude = lattitude, longitude = longitude)
                checkin_date = attendence.date
                if(checkin_date == date):
                    attendence_serializer = MyAttendenceSerializer(attendence, data={
                    "check_out_time" : time
                    }, partial = True)
                    if attendence_serializer.is_valid():
                        attendence_serializer.save()
                        try:
                            name = request.user.name
                            user_email = request.user.email
                            email_1 = EmailMessage(f"{name}", f" Check Out Successfully at {time}", 'simply2cloud@gmail.com',["positive.mind.123456789@gmail.com"])
                            email_2 = EmailMessage("You CheckOut Successfully", f"You check Out at {time}", 'simply2cloud@gmail.com',[user_email])
                            email_1.send()
                            email_2.send()
                        except Exception as e:
                            print("email failed")
                            print(e)
                        return Response({"message" : "Checkout Successfully!"}, status=status.HTTP_200_OK)
                    else:
                        return Response(attendence_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error" : "Checkout should on the same day"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal server error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDataMonthWise(APIView):
    def get(self, request, id = None):
        try:
            if id is not None:
                if(request.user.id == id or request.user.is_superuser):
                    user = EmployeeUser.objects.get(id = id)
                    year = int(request.GET.get("year"))
                    month = datetime.strptime(request.GET.get("month"), '%B').month
                    month_data = attendance_data_func_month(user, month, year)
                    return Response(month_data, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error" : "Internal server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)