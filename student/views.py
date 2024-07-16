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


# Create your views here.
class StudentApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if id is not None:
                if request.user.is_admin:
                    student = Student.objects.filter(Q(batch_id = id) & Q(active = True))
                else:
                    student = Student.objects.filter(Q(batch_id = id) & Q(active = True) & Q(batch_id__assigned_to = request.user.id))
                student_serializer = StudentSerialzer(student, many = True)
                for i in student_serializer.data:
                    i['batch_id'] = BatchModel.objects.get(id = i['batch_id']).batch_name
                return Response(student_serializer.data, status=status.HTTP_200_OK)
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
            else:
                student = Student.objects.filter(Q(active = True)) if request.user.is_admin else  Student.objects.filter(Q(active = True) & (Q(batch_id__assigned_to = request.user.id)))
                student_serializer = StudentSerialzer(student , many = True)
                for i in student_serializer.data:
                    i['batch_id'] = BatchModel.objects.get(id = i['batch_id']).batch_name
                return Response(student_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, id = None):
        try:    
            student_serializer = StudentSerialzer(data={**request.data, "added_by" : request.user.id})
            if student_serializer.is_valid():
                student_serializer.save()
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
