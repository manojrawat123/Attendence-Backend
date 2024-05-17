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
from employee.views import MyEmployeeLoginView, CheckEmailApi, CreateEmployeeUserView,GetUserInfoAdmin, ProfileView
from attendence_tracer.views import CheckInView, GetDataMonthWise
from leave.views import GetLeaveApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyEmployeeLoginView.as_view(), name= "login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('register/', CreateEmployeeUserView.as_view(), name = "register"),
    path('emailcheck/', CheckEmailApi.as_view(), name = "Email Check"),
    path('checkin/', CheckInView.as_view(), name = "Check In User"),
    path('checkin/<int:id>/', CheckInView.as_view(), name = "Check out User"),
    path('leave/', GetLeaveApiView.as_view(), name = "Leave Api View"),
    path('leave/<int:id>/', GetLeaveApiView.as_view(), name = "Leave Api View"),
    path('get_employee_detail/', GetUserInfoAdmin.as_view(), name = "Get User Information"),
    path('get_month_data/', GetDataMonthWise.as_view(), name = "Get Month Data"),
    path('get_month_data/<int:id>/', GetDataMonthWise.as_view(), name = "Get Month Data"),
]