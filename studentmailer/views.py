from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from batch.models import BatchModel
from batch.serializer import BatchSerializer
from student.models import Student
from django.core.mail import EmailMessage
from studentmailer.serializer import StudentMailerSerializer
from django.db.models import Q
from emailtemplate.models import EmailTemplate
from emailtemplate.serializer import EmailTemplateSerializer

class SendMailStudentView(APIView):
    def get(self, request, id = None):
        try:
            if request.GET.get('page') == 'page':
                # Batch Detail
                batch = BatchModel.objects.filter(active = True) if request.user.is_admin else  BatchModel.objects.filter(( Q(assigned_to = request.user.id) ) & Q(active = True))
                batch_serializer = BatchSerializer(batch, many = True)
                
                # Email Template
                emailtemplate = EmailTemplate.objects.filter(display = True)
                email_template_serilaizer = EmailTemplateSerializer(emailtemplate, many = True)

                return Response({
                    "batch" : batch_serializer.data,
                    'email_template' : email_template_serilaizer.data
                })
            else:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({}, )
    def post(self, request, id = None):
        if id is not None:
            return Response({"error": "Method Not Allowed"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            try:
                student_email_list = Student.objects.filter(batch_id = request.data.get('batch_id')).values_list('student_email', flat=True) 
                student_email = EmailMessage(f"{request.data.get('subject')}",f"{request.data.get('body')} \n {request.data.get('signature')}",'simply2cloud@gmail.com',student_email_list)
                student_email.send()
                student_email_serializer = StudentMailerSerializer(data = request.data)
                if student_email_serializer.is_valid():
                    student_email_serializer.save()
                    return Response({"message" : "Data Saved Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(student_email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
