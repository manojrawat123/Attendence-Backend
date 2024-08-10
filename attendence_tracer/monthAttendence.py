from datetime import datetime
import calendar
from attendence_tracer.models import Attendence
from leave.models import Leave

def attendance_data_func_month(user, month, year):
    attendance_month_data = {}

    days = calendar.monthrange(year, month)[1]

    attendance_records = Attendence.objects.filter(
        employee_user=user,
        date__year=year,
        date__month=month
    )

    leave_dates = Leave.objects.filter(
        employee_user=user,
        date__year=year,
        date__month=month
    ).values_list('date', flat=True)

    for day in range(1, days + 1):
        date = datetime(year, month, day)
        check_in_time = None
        check_out_time = None

        # Check if there's an attendance record for this day
        attendance_record = attendance_records.filter(date=date).first()        
       
        if attendance_record:
            check_in_time = attendance_record.check_in_time
            check_out_time = attendance_record.check_out_time
        # Check if the day is marked as leave
        leave = date.date() in leave_dates
        # Construct attendance data dictionary for the day
        day_attendance_data = {
            "checkinTime": check_in_time.strftime("%I:%M%p") if check_in_time else None,
            "checkoutTime": check_out_time.strftime("%I:%M%p") if check_out_time else None,
            "leave": leave
        }
        
        # Add attendance data to the main dictionary
        attendance_month_data[date.strftime("%d %b %Y")] = day_attendance_data    
        
    return attendance_month_data