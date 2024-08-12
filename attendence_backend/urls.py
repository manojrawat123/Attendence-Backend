"""attendence_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employee.views import MyEmployeeLoginView, CheckEmailApi, CreateEmployeeUserView,GetUserInfoAdmin, ProfileView,ForgotPassword, ResetPassword
from attendence_tracer.views import CheckInView, GetDataMonthWise
from leave.views import GetLeaveApiView
from batch.views import BatchGetView
from student.views import StudentApiView
from studentattendence.views import StudentAttendenceView
from studentmailer.views import SendMailStudentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyEmployeeLoginView.as_view(), name= "login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/<int:id>/', ProfileView.as_view(), name="profile"),
    path('register/', CreateEmployeeUserView.as_view(), name = "register"),
    path('emailcheck/', CheckEmailApi.as_view(), name = "Email Check"),
    path('checkin/', CheckInView.as_view(), name = "Check In User"),
    path('checkin/<int:id>/', CheckInView.as_view(), name = "Check out User"),
    path('leave/', GetLeaveApiView.as_view(), name = "Leave Api View"),
    path('leave/<int:id>/', GetLeaveApiView.as_view(), name = "Leave Api View"),
    path('get_employee_detail/', GetUserInfoAdmin.as_view(), name = "Get User Information"),
    path('get_month_data/', GetDataMonthWise.as_view(), name = "Get Month Data"),
    path('get_month_data/<int:id>/', GetDataMonthWise.as_view(), name = "Get Month Data"),
    path('batch/', BatchGetView.as_view(), name = "batch-get-view"),
    path('batch/<int:id>/', BatchGetView.as_view(), name = "batch-update-delete-view"),
    path('student/', StudentApiView.as_view(), name = "student-get-view"),
    path('student/<int:id>/', StudentApiView.as_view(), name = "student-update-delete-view"),
    path('studentattendence/', StudentAttendenceView.as_view(), name = "student-update-delete-view"),
    path('studentattendence/<int:id>/', StudentAttendenceView.as_view(), name = "student-update-delete-view"),
    path('reset-password/<userid_encode>/<token>/', ResetPassword.as_view(), name="Reset Password"),
    path('forgetpassword/', ForgotPassword.as_view(), name="forgot password email"),
    path('sendmail/', SendMailStudentView.as_view(), name="forgot password email"),

]