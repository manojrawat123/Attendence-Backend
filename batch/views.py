from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from employee.models import EmployeeUser
from employee.serializers import MyEmployeeSerializer
from rest_framework import status
from mybrand.serializer import BrandSerializer
from mybrand.models import Brand
from batch.serializer import BatchSerializer
from batch.models import BatchModel
from django.db.models import Q

# Create your views here.
class BatchGetView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if request.GET.get('page') == 'page':
                if request.user.is_admin:
                    employee = EmployeeUser.objects.all()
                    brand = Brand.objects.all()
                else:
                    employee = EmployeeUser.objects.filter(id = request.user.id)
                    brand = Brand.objects.filter(id = request.user.brand_name.id)
                brand_serializer = BrandSerializer(brand, many = True)
                employee_serializer = MyEmployeeSerializer(employee, many = True)
                return Response(
                {
                    "user" : employee_serializer.data,
                    "brand" : brand_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                batch = BatchModel.objects.filter(active = True) if request.user.is_admin else  BatchModel.objects.filter(( Q(assigned_to = request.user.id) ) & Q(active = True))
                batch_serializer = BatchSerializer(batch, many = True)
                for i in batch_serializer.data:
                    i['teacher'] = EmployeeUser.objects.get(id = i['assigned_to']).name
                    i['brand_name'] = Brand.objects.get(id = i['brand']).brand_name
                    batch_start_time = i['batch_start_timing'][:5]
                    batch_end_time = i['batch_end_timing'][:5]
                    i['batch_timing'] = f'{batch_start_time} - {batch_end_time}'
                return Response(batch_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, id = None):
        try:    
            batch_serializer = BatchSerializer(data={**request.data, "created_by" : request.user.id})
            if batch_serializer.is_valid():
                batch_serializer.save()
                return Response({
                    "message" : "Batch Added Successfully"
                }, status=status.HTTP_200_OK)
            else:
                return Response(batch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            batch = BatchModel.objects.get(id = id)
            batch_serializer = BatchSerializer(batch , data=request.data, partial = True)
            if batch_serializer.is_valid():
                batch_serializer.save()
                return Response({"message" : "Batch Updated Successfully"}, status=status.HTTP_200_OK)

            else:
                return Response(batch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id = None):
        try:
            batch = BatchModel.objects.get(id = id)
            batch.active = not batch.active
            batch.save()
            return Response({"message" : "Successfully Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({ "error" : "Internal Server Error" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


