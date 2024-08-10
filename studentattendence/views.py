from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from django.db.models import Q,Count
from student.serializer import StudentSerialzer
from batch.models import BatchModel
from studentattendence.models import Attendance
from studentattendence.serializer import StudentAttendenceSerializer
from django.utils import timezone
from emailtemplate.models import EmailTemplate
from django.core.mail import EmailMultiAlternatives
from datetime import datetime



today = datetime.today()

            # Format the date in a readable format
formatted_date = today.strftime("%A, %B %d, %Y")

# Create your views here.
class StudentAttendenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id = None):
        try:
            batch_id = request.GET.get('batch')
            if request.GET.get('batch') is not None:
                if request.GET.get('page') == 'display':
                    student =  Student.objects.filter(Q(batch_id = batch_id)) if request.user.is_admin else  Student.objects.filter(Q(batch_id = request.GET.get('batch')) & Q(batch_id__assigned_to = request.user.id)) 
                    student_serializer = StudentSerialzer(student, many = True)
                    return Response({
                        "student" : student_serializer.data
                    }, status=status.HTTP_200_OK)

                elif request.GET.get('page') == 'attendencepost':
                    batch_student = Student.objects.filter(
                        Q(active = True) & Q(batch_id = batch_id)) if request.user.is_admin else Student.objects.filter(
                        Q(active = True) & Q(batch_id = batch_id) & Q(batch_id__assigned_to = request.user.id))
                    batch_student_serializer = StudentSerialzer(batch_student, many = True)
                    
                    # Attendence Obj
                    attendence_obj = Attendance.objects.filter(Q(batch_id = batch_id) & Q(date = timezone.now().date()))
                    attendence =  attendence_obj if request.user.is_admin else attendence_obj.filter(Q(batch_id__assigned_to = request.user.id))
                    attendence_serializer = StudentAttendenceSerializer(attendence, many = True)
                    if len(attendence_serializer.data) == 0:
                        return Response({
                            'status' : "pending",
                            'batch_student' : batch_student_serializer.data,
                            "attendence"  : attendence_serializer.data
                            }, status=status.HTTP_200_OK)
                    else:
                        for i in attendence_serializer.data:
                            student_detail = Student.objects.get(id = i['student'])
                            s_student_serializer = StudentSerialzer(student_detail)
                            i['student_detail'] = s_student_serializer.data
                        return Response({
                            'status' : 'done',
                            'batch_student' : batch_student_serializer.data,
                            "attendence"  : attendence_serializer.data
                        })                     

                elif request.GET.get('page') == 'attendenceget':
                    student = Student.objects.filter(Q(batch_id=batch_id)) if request.user.is_admin else Student.objects.filter(
                        Q(batch_id=request.GET.get('batch')) & Q(batch_id__assigned_to=request.user.id))

                    # Serialize the students
                    student_serializer = StudentSerialzer(student, many=True)

                    # Get student IDs
                    student_ids = [student['id'] for student in student_serializer.data]

                    # Annotate attendance data
                    attendance_aggregated = Attendance.objects.filter(student__in=student_ids).values('student').annotate(
                        total_days=Count('id'),
                        present=Count('id', filter=Q(attendance_status="Present")),
                        absent=Count('id', filter=Q(attendance_status="Absent"))
                    )

                    # Create a dictionary for easy access
                    attendance_dict = {item['student']: item for item in attendance_aggregated}

                    # Update the serialized student data
                    for student in student_serializer.data:
                        student_id = student['id']
                        student['total_days'] = attendance_dict.get(student_id, {}).get('total_days', 0)
                        student['present'] = attendance_dict.get(student_id, {}).get('present', 0)
                        student['absent'] = attendance_dict.get(student_id, {}).get('absent', 0)

                    return Response(student_serializer.data)
            return Response({"error" : "Invalid Request"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error' : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request , id = None):
        try:
            batch = BatchModel.objects.get(id = request.data.get('batch_id'))
            
            for i in request.data.get('present_student'):
                attendence_serializer = StudentAttendenceSerializer(data={
                    'batch_id' : request.data.get('batch_id'),
                    'student' : i,
                    'attendance_status' : "Present"  
                    })
                if attendence_serializer.is_valid():
                    attendence_serializer.save()
                else:
                    print('error')
            for i in request.data.get('absent_student'):
                attendence_serializer = StudentAttendenceSerializer(data={
                    'batch_id' : request.data.get('batch_id'),
                    'student' : i,
                    'attendance_status' : "Absent"  
                    })
                if attendence_serializer.is_valid():
                    attendence_serializer.save()
                    try:
                        email = EmailTemplate.objects.get(id = 2)
                        student = Student.objects.get(id = i)
                        
                        subject = email.subject.replace('batch_name', batch.batch_name).replace('brand_name', request.user.brand_name.brand_name)
                        message = email.template_body.replace('student', student.student_name).replace('batch_name' , batch.batch_name).replace('today', formatted_date).replace('brand_name', request.user.brand_name.brand_name) + "\n" + email.signature
                        
                        email = EmailMultiAlternatives(
                                    subject, 
                                    "",    
                                    'simply2cloud@gmail.com',  
                                    # ['bahimunna457@gmail.com']
                                    [student.student_email]            
                                )
                        # Attach the HTML content
                        email.attach_alternative(message, "text/html")
                        email.send()
                    except Exception as e:
                        print(e)
                else:
                    print('error')
            return Response("Data Updated Successfully!!")      
        except Exception as e:
            print(e)
            return Response({'error' : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id = None):
        try:
            student_attendence = Attendance.objects.get(id = id)
            attendence_serializer = StudentAttendenceSerializer(student_attendence, data=request.data, partial= True)
            if attendence_serializer.is_valid():
                attendence_serializer.save()
                if (student_attendence.attendance_status == "Absent"):
                    try:
                            email = EmailTemplate.objects.get(id = 2)
                            
                            subject = email.subject.replace('batch_name', student_attendence.batch_id.batch_name).replace('brand_name', request.user.brand_name.brand_name)
                            message = email.template_body.replace('student', student_attendence.student.student_name).replace('batch_name' , student_attendence.batch_id.batch_name).replace('today', formatted_date).replace('brand_name', request.user.brand_name.brand_name) + "\n" + email.signature
                            
                            email = EmailMultiAlternatives(
                                        subject, 
                                        "",    
                                        'simply2cloud@gmail.com',  
                                        # ['bahimunna457@gmail.com']
                                        [student_attendence.student.student_email]            
                                    )
                            # Attach the HTML content
                            email.attach_alternative(message, "text/html")
                            email.send()
                    except Exception as e:
                        print(e)
                print(request.data)
                return Response({"message" : "Updated Successfully"},status=status.HTTP_200_OK)
            else:
                return Response(attendence_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

