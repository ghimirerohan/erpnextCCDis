import frappe
from frappe import _
from datetime import datetime, timedelta
import json

# Import nepali date utilities if available
try:
    from nepal_compliance.utils.nepali_date import ad_to_bs
except ImportError:
    def ad_to_bs(date_str):
        """Fallback function if nepal_compliance is not available"""
        try:
            from nepali_datetime import date as NepaliDate
            if isinstance(date_str, str):
                ad_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                ad_date = date_str
            nd = NepaliDate.from_datetime_date(ad_date)
            return nd.strftime("%Y-%m-%d")
        except:
            # Simple approximation if library not available
            if isinstance(date_str, str):
                ad_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                ad_date = date_str
            # Rough conversion (57 years difference)
            bs_year = ad_date.year + 57
            return f"{bs_year}-{ad_date.month:02d}-{ad_date.day:02d}"


def get_employee_time_for_date(employee, date):
    """
    Get in and out time for an employee on a specific date.
    In = first checkin of the day
    Out = last checkin of the day
    """
    checkins = frappe.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "time": ["between", [f"{date} 00:00:00", f"{date} 23:59:59"]]
        },
        fields=["time", "log_type"],
        order_by="time asc"
    )
    
    in_time = None
    out_time = None
    
    if checkins:
        # First checkin is IN time
        in_time = checkins[0].time
        # Last checkin is OUT time (if different from first)
        if len(checkins) > 1:
            out_time = checkins[-1].time
    
    return in_time, out_time


def format_time(dt):
    """Format datetime to HH:MM string"""
    if dt:
        if isinstance(dt, str):
            dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%H:%M")
    return None


def check_late_entry(in_time, shift_start="09:00"):
    """Check if the entry is late based on shift start time"""
    if not in_time:
        return False
    
    # Validate shift_start
    if not shift_start or ':' not in str(shift_start):
        shift_start = "09:00"
    
    if isinstance(in_time, str):
        in_time = datetime.strptime(in_time, "%Y-%m-%d %H:%M:%S")
    
    # Parse shift start time safely
    try:
        parts = str(shift_start).split(":")
        shift_hour = int(parts[0])
        shift_minute = int(parts[1]) if len(parts) > 1 else 0
    except (ValueError, IndexError):
        shift_hour, shift_minute = 9, 0  # Default to 9:00 AM
    
    shift_start_dt = in_time.replace(hour=shift_hour, minute=shift_minute, second=0)
    
    # Allow 5 minutes grace period
    grace_minutes = 5
    shift_start_with_grace = shift_start_dt + timedelta(minutes=grace_minutes)
    
    return in_time > shift_start_with_grace


def check_early_exit(out_time, shift_end="18:00"):
    """Check if the exit is early based on shift end time"""
    if not out_time:
        return False
    
    # Validate shift_end
    if not shift_end or ':' not in str(shift_end):
        shift_end = "18:00"
    
    if isinstance(out_time, str):
        out_time = datetime.strptime(out_time, "%Y-%m-%d %H:%M:%S")
    
    # Parse shift end time safely
    try:
        parts = str(shift_end).split(":")
        shift_hour = int(parts[0])
        shift_minute = int(parts[1]) if len(parts) > 1 else 0
    except (ValueError, IndexError):
        shift_hour, shift_minute = 18, 0  # Default to 6:00 PM
    
    shift_end_dt = out_time.replace(hour=shift_hour, minute=shift_minute, second=0)
    
    # Allow 5 minutes grace period
    grace_minutes = 5
    shift_end_with_grace = shift_end_dt - timedelta(minutes=grace_minutes)
    
    return out_time < shift_end_with_grace


def format_timedelta_to_time_str(td):
    """Convert timedelta or time string to HH:MM format"""
    if td is None:
        return None
    
    # Handle timedelta objects
    if hasattr(td, 'total_seconds'):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    
    # Handle string - ensure proper HH:MM format
    time_str = str(td)
    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) >= 2:
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                return f"{hours:02d}:{minutes:02d}"
            except ValueError:
                pass
    
    return None


def get_shift_times(employee, date):
    """Get shift start and end times for an employee"""
    shift_start = "09:00"
    shift_end = "18:00"
    
    # Try to get shift assignment for the employee
    shift_assignment = frappe.get_all(
        "Shift Assignment",
        filters={
            "employee": employee,
            "start_date": ["<=", date],
            "docstatus": 1,
            "status": "Active"
        },
        fields=["shift_type"],
        order_by="start_date desc",
        limit=1
    )
    
    if shift_assignment:
        shift_type = frappe.get_doc("Shift Type", shift_assignment[0].shift_type)
        if shift_type.start_time:
            formatted = format_timedelta_to_time_str(shift_type.start_time)
            if formatted:
                shift_start = formatted
        if shift_type.end_time:
            formatted = format_timedelta_to_time_str(shift_type.end_time)
            if formatted:
                shift_end = formatted
    else:
        # Try to get default shift
        default_shift = frappe.get_all(
            "Shift Type",
            filters={"name": "Default"},
            fields=["start_time", "end_time"],
            limit=1
        )
        if default_shift:
            if default_shift[0].start_time:
                formatted = format_timedelta_to_time_str(default_shift[0].start_time)
                if formatted:
                    shift_start = formatted
            if default_shift[0].end_time:
                formatted = format_timedelta_to_time_str(default_shift[0].end_time)
                if formatted:
                    shift_end = formatted
    
    return shift_start, shift_end


@frappe.whitelist()
def get_attendance_list(date=None):
    """
    Get attendance list for all employees for a given date.
    Returns employee details with attendance status, in/out times, and late/early flags.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Get all active employees
    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "employee_name", "department", "designation", "company"]
    )
    
    result = []
    summary = {
        "total": len(employees),
        "present": 0,
        "absent": 0,
        "checked_in": 0,  # Employees with checkin but no attendance record yet (real-time)
        "on_time_entry": 0,
        "late_entry": 0,
        "early_exit": 0,
        "on_time_exit": 0,
    }
    
    for emp in employees:
        # Get attendance record for the date
        attendance = frappe.get_all(
            "Attendance",
            filters={
                "employee": emp.name,
                "attendance_date": date,
                "docstatus": ["!=", 2]  # Not cancelled
            },
            fields=["name", "status", "in_time", "out_time", "late_entry", "early_exit"],
            limit=1
        )
        
        emp_data = {
            "employee": emp.name,
            "employee_name": emp.employee_name,
            "department": emp.department,
            "designation": emp.designation,
            "company": emp.company,
            "status": "Absent",
            "in_time": None,
            "out_time": None,
            "late_entry": False,
            "early_exit": False,
        }
        
        if attendance:
            att = attendance[0]
            emp_data["status"] = att.status
            emp_data["in_time"] = format_time(att.in_time)
            emp_data["out_time"] = format_time(att.out_time)
            emp_data["late_entry"] = bool(att.late_entry)
            emp_data["early_exit"] = bool(att.early_exit)
            
            if att.status == "Present":
                summary["present"] += 1
                if att.late_entry:
                    summary["late_entry"] += 1
                else:
                    summary["on_time_entry"] += 1
                if att.early_exit:
                    summary["early_exit"] += 1
                else:
                    summary["on_time_exit"] += 1
            elif att.status == "Half Day":
                summary["present"] += 1  # Count half day as present
                if att.late_entry:
                    summary["late_entry"] += 1
            else:
                summary["absent"] += 1
        else:
            # No attendance record - check for checkins
            in_time, out_time = get_employee_time_for_date(emp.name, date)
            
            if in_time or out_time:
                # Has checkins but no attendance created - REAL-TIME check-in visibility
                emp_data["in_time"] = format_time(in_time)
                emp_data["out_time"] = format_time(out_time)
                emp_data["status"] = "Checked In"  # More descriptive than "Checkin Only"
                
                # Check late/early based on shift
                shift_start, shift_end = get_shift_times(emp.name, date)
                emp_data["late_entry"] = check_late_entry(in_time, shift_start)
                emp_data["early_exit"] = check_early_exit(out_time, shift_end)
                
                # Count in summary for real-time visibility
                summary["checked_in"] += 1
                if emp_data["late_entry"]:
                    summary["late_entry"] += 1
                else:
                    summary["on_time_entry"] += 1
            else:
                summary["absent"] += 1
        
        result.append(emp_data)
    
    # Sort by status (Present first, then Checked In, then Half Day, then others)
    status_order = {"Present": 0, "Checked In": 1, "Half Day": 2, "On Leave": 3, "Absent": 4}
    result.sort(key=lambda x: (status_order.get(x["status"], 5), x["employee_name"]))
    
    return {
        "success": True,
        "data": result,
        "summary": summary,
        "date": date,
        "date_bs": ad_to_bs(date)
    }


@frappe.whitelist()
def get_employee_history(employee, days=7):
    """
    Get attendance history for a specific employee for the past N days.
    """
    days = int(days)
    
    # Get employee info
    emp_info = frappe.get_doc("Employee", employee)
    employee_info = {
        "employee": emp_info.name,
        "employee_name": emp_info.employee_name,
        "department": emp_info.department,
        "designation": emp_info.designation,
    }
    
    # Calculate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)
    
    result = []
    summary = {
        "present": 0,
        "absent": 0,
        "late_entries": 0,
        "early_exits": 0,
    }
    
    # Get all attendance records within the date range
    attendance_records = frappe.get_all(
        "Attendance",
        filters={
            "employee": employee,
            "attendance_date": ["between", [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]],
            "docstatus": ["!=", 2]
        },
        fields=["name", "attendance_date", "status", "in_time", "out_time", "late_entry", "early_exit"],
        order_by="attendance_date desc"
    )
    
    # Get all checkins without attendance within the date range
    checkin_records = frappe.db.sql("""
        SELECT DISTINCT DATE(time) as date, employee
        FROM `tabEmployee Checkin`
        WHERE employee = %s
        AND DATE(time) BETWEEN %s AND %s
        AND NOT EXISTS (
            SELECT 1 FROM `tabAttendance` a
            WHERE a.employee = `tabEmployee Checkin`.employee
            AND a.attendance_date = DATE(`tabEmployee Checkin`.time)
            AND a.docstatus != 2
        )
    """, (employee, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")), as_dict=True)
    
    # Create a set of dates that have records
    dates_with_records = set()
    
    # Process attendance records
    for att in attendance_records:
        date_str = att.attendance_date.strftime("%Y-%m-%d") if hasattr(att.attendance_date, 'strftime') else str(att.attendance_date)
        dates_with_records.add(date_str)
        
        record = {
            "date": date_str,
            "date_bs": ad_to_bs(date_str),
            "status": att.status,
            "in_time": format_time(att.in_time),
            "out_time": format_time(att.out_time),
            "late_entry": bool(att.late_entry),
            "early_exit": bool(att.early_exit),
        }
        
        if att.status in ["Present", "Half Day"]:
            summary["present"] += 1
        else:
            summary["absent"] += 1
        
        if att.late_entry:
            summary["late_entries"] += 1
        if att.early_exit:
            summary["early_exits"] += 1
        
        result.append(record)
    
    # Process checkins without attendance
    for checkin in checkin_records:
        date_str = checkin.date.strftime("%Y-%m-%d") if hasattr(checkin.date, 'strftime') else str(checkin.date)
        if date_str in dates_with_records:
            continue  # Skip if already has attendance record
        
        dates_with_records.add(date_str)
        
        in_time, out_time = get_employee_time_for_date(employee, date_str)
        if in_time or out_time:
            shift_start, shift_end = get_shift_times(employee, date_str)
            late_entry = check_late_entry(in_time, shift_start) if in_time else False
            early_exit = check_early_exit(out_time, shift_end) if out_time else False
            
            record = {
                "date": date_str,
                "date_bs": ad_to_bs(date_str),
                "status": "Checked In",
                "in_time": format_time(in_time),
                "out_time": format_time(out_time),
                "late_entry": late_entry,
                "early_exit": early_exit,
            }
            
            if late_entry:
                summary["late_entries"] += 1
            if early_exit:
                summary["early_exits"] += 1
            
            result.append(record)
    
    # Sort by date descending (most recent first)
    result.sort(key=lambda x: x["date"], reverse=True)
    
    return {
        "success": True,
        "employee_info": employee_info,
        "data": result,
        "summary": summary,
        "days": days
    }


@frappe.whitelist()
def sync_attendance(date=None):
    """
    Sync attendance by processing employee checkins that don't have attendance records.
    Uses the shift type's mark_attendance_from_checkins functionality.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Get all employee checkins for the date that don't have attendance
    checkins = frappe.db.sql("""
        SELECT DISTINCT ec.employee, ec.time
        FROM `tabEmployee Checkin` ec
        LEFT JOIN `tabAttendance` a ON (
            a.employee = ec.employee 
            AND a.attendance_date = %s 
            AND a.docstatus != 2
        )
        WHERE DATE(ec.time) = %s
        AND a.name IS NULL
        ORDER BY ec.employee
    """, (date, date), as_dict=True)
    
    if not checkins:
        return {
            "success": True,
            "message": "No checkins left to process",
            "processed": 0
        }
    
    # Get unique employees with unprocessed checkins
    employees_to_process = list(set([c.employee for c in checkins]))
    
    processed_count = 0
    errors = []
    
    for employee in employees_to_process:
        try:
            # Get in and out time for the employee
            in_time, out_time = get_employee_time_for_date(employee, date)
            
            if not in_time:
                continue
            
            # Check if attendance already exists (double check)
            existing = frappe.db.exists("Attendance", {
                "employee": employee,
                "attendance_date": date,
                "docstatus": ["!=", 2]
            })
            
            if existing:
                continue
            
            # Get shift times
            shift_start, shift_end = get_shift_times(employee, date)
            
            # Check late entry and early exit
            late_entry = check_late_entry(in_time, shift_start)
            early_exit = check_early_exit(out_time, shift_end) if out_time else False
            
            # Determine status
            status = "Present"
            if late_entry and early_exit:
                status = "Half Day"
            
            # Create attendance record
            attendance = frappe.new_doc("Attendance")
            attendance.employee = employee
            attendance.attendance_date = date
            attendance.status = status
            attendance.in_time = in_time
            attendance.out_time = out_time
            attendance.late_entry = 1 if late_entry else 0
            attendance.early_exit = 1 if early_exit else 0
            
            # Try to get shift assignment
            shift_assignment = frappe.get_all(
                "Shift Assignment",
                filters={
                    "employee": employee,
                    "start_date": ["<=", date],
                    "docstatus": 1,
                    "status": "Active"
                },
                fields=["shift_type"],
                order_by="start_date desc",
                limit=1
            )
            
            if shift_assignment:
                attendance.shift = shift_assignment[0].shift_type
            else:
                # Try default shift
                default_shift = frappe.db.exists("Shift Type", "Default")
                if default_shift:
                    attendance.shift = "Default"
            
            attendance.insert(ignore_permissions=True)
            attendance.submit()
            
            processed_count += 1
            
        except Exception as e:
            errors.append(f"Employee {employee}: {str(e)}")
            frappe.log_error(f"Attendance sync error for {employee}: {str(e)}", "Attendance Sync")
    
    message = f"Processed {processed_count} attendance record(s)"
    if errors:
        message += f". {len(errors)} error(s) occurred."
    
    frappe.db.commit()
    
    return {
        "success": True,
        "message": message,
        "processed": processed_count,
        "errors": errors if errors else None
    }


@frappe.whitelist()
def get_pending_checkins_count(date=None):
    """
    Get count of employee checkins that don't have attendance records.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    count = frappe.db.sql("""
        SELECT COUNT(DISTINCT ec.employee) as count
        FROM `tabEmployee Checkin` ec
        LEFT JOIN `tabAttendance` a ON (
            a.employee = ec.employee 
            AND a.attendance_date = %s 
            AND a.docstatus != 2
        )
        WHERE DATE(ec.time) = %s
        AND a.name IS NULL
    """, (date, date), as_dict=True)
    
    return {
        "success": True,
        "count": count[0].count if count else 0,
        "date": date
    }

