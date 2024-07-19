from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from batch.models import BatchModel
from batch.serializer import BatchSerializer
from student.models import Student
from student.serializer import StudentSerialzer
from employee.models import EmployeeUser
from employee.serializers import MyEmployeeSerializer
from studentattendence.models import Attendance
from studentattendence.serializer import StudentAttendenceSerializer
from django.utils import timezone


# Create your views here.
class StudentApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if id is not None:
                if request.user.is_admin:
                    student = Student.objects.filter(Q(batch_id = id) & Q(active = True))
                    batch = BatchModel.objects.filter(Q(active = True))
                else:
                    student = Student.objects.filter(Q(batch_id = id) & Q(active = True) & Q(batch_id__assigned_to = request.user.id))
                    batch = BatchModel.objects.filter(Q(active = True) & Q(assigned_to = request.user.id))
                batch_serializer = BatchSerializer(batch, many = True)
                student_serializer = StudentSerialzer(student, many = True)
                for i in student_serializer.data:
                    i['batch_name'] = BatchModel.objects.get(id = i['batch_id']).batch_name
                return Response({
                                    'student' : student_serializer.data,
                                    'batch' : batch_serializer.data
                                }, status=status.HTTP_200_OK)
            if request.GET.get('page') == 'page':
                if request.user.is_admin:
                    batch =  BatchModel.objects.filter(active = True)
                    employee = EmployeeUser.objects.filter(is_active = True)
                else:
                    batch =  BatchModel.objects.filter(Q(active = True) & Q(assigned_to = request.user.id))
                    employee = EmployeeUser.objects.filter(Q(id = request.user.id) & Q(is_active = True))
                employee_serializer = MyEmployeeSerializer(employee, many = True)
                batch_serializer = BatchSerializer(batch, many = True)
                for i in batch_serializer.data:
                    batch_created_by = EmployeeUser.objects.get(id = i['assigned_to']).name
                    i['assigned_to'] = batch_created_by
                return Response({
                    "batch" : batch_serializer.data,
                    "employee" : employee_serializer.data
                }, status=status.HTTP_200_OK)
            elif(request.GET.get('display')):
                batch_id = request.GET.get('batch_id')
                if batch_id is None:
                    return Response({"error" : "Batch Id is not provided"}, status=status.HTTP_400_BAD_REQUEST)
                student = Student.objects.filter(Q(active = True) & Q(batch_id =batch_id )) if request.user.is_admin else  Student.objects.filter(Q(active = True)  & Q(batch_id = batch_id ) & (Q(batch_id__assigned_to = request.user.id)))
                batch =  BatchModel.objects.filter(active = True) if request.user.is_admin else BatchModel.objects.filter(Q(active = True) & Q(assigned_to = request.user.id))
                batch_serializer = BatchSerializer(batch, many = True)
                student_serializer = StudentSerialzer(student , many = True)
                for i in student_serializer.data:
                    i['batch_name'] = BatchModel.objects.get(id = i['batch_id']).batch_name
                return Response({
                    'student' : student_serializer.data,
                    'batch' : batch_serializer.data
                    }, status=status.HTTP_200_OK)
            return Response({'error' : "Invalid Response"})
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, id = None):
        try:    
            student_serializer = StudentSerialzer(data={**request.data, "added_by" : request.user.id})            
            if student_serializer.is_valid():
                student = student_serializer.save()
                try:
                    attendence_obj = Attendance.objects.filter(Q(batch_id = request.data.get('batch_id')) & Q(date = timezone.now().date()))
                    attendence =  attendence_obj if request.user.is_admin else attendence_obj.filter(Q(batch_id__assigned_to = request.user.id))
                    attendence_serializer = StudentAttendenceSerializer(attendence, many = True)
                    if len(attendence_serializer.data) != 0:
                        new_student_attendence_serialzer = StudentAttendenceSerializer(data={'student' : student.id,
                                                                                         'batch_id' : request.data.get('batch_id'),
                                                                                         'attendance_status' : "Present"
                                                                                         })
                        if new_student_attendence_serialzer.is_valid():
                            new_student_attendence_serialzer.save()
                            return Response(new_student_attendence_serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print(e)

                return Response({
                    "message" : "Student Added Successfully"
                }, status=status.HTTP_200_OK)
            else:
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            student = Student.objects.get(id = id)
            student_serializer = StudentSerialzer(student , data=request.data, partial = True)
            if student_serializer.is_valid():
                student_serializer.save()
                return Response({"message" : "student Updated Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, id = None):
        try:
            student = Student.objects.get(id = id)
            student.active = not student.active
            student.save()
            return Response({"message" : "Successfully Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({ "error" : "Internal Server Error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

