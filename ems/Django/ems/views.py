from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Employee, Department, Salary, Attendance
# Create your views here.


def index(request):
    return render(request, 'index.html')


def admin_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user and user.is_admin:
            login(request, user)
            request.session['username'] = email
            return redirect("employee_info")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def employee_add(request):
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        position = request.POST['position']
        department_name = request.POST['department']
        phone = request.POST['phone']
        if not email or not name or not age or not position or not department_name or not phone:
            return render(request, 'department_add.html', {'error': '所有字段都是必填的'})
        employee = Employee(
            email=email,
            name=name,
            gender=gender,
            age=age,
            position=position,
            department_name=department_name,
            phone=phone
        )
        employee.save()
        # 重定向到员工信息页面
        return redirect('employee_info')
    return render(request, 'employee_add.html')


@login_required
def employee_delete(request):
    if request.method == "POST":
        user_id = request.POST['id']
        employee = get_object_or_404(Employee, id=user_id)
        try:
            department = Department.objects.get(manager_id=employee.id)
            if department:
                department.manager_id = None
                department.manager_name = None
                department.save()
        except Department.DoesNotExist:
            pass
        salaries = Salary.objects.filter(employee_id=employee.id)
        if len(salaries) > 0:
            salaries.delete()
        else:
            pass
        attendances = Attendance.objects.filter(employee_id=employee.id)
        if len(attendances) > 0:
            attendances.delete()
        else:
            pass
        employee.delete()
        return redirect('employee_info')
    return render(request, 'employee_delete.html')


@login_required
def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        employee.email = request.POST['email']
        employee.name = request.POST['name']
        employee.gender = request.POST['gender']
        employee.age = request.POST['age']
        employee.position = request.POST['department']
        employee.phone = request.POST['phone']
        if not employee.email or not employee.name or not employee.gender or not employee.age or not employee.position or not employee.phone:
            return render(request, 'employee_edit.html', {'error': '所有字段都是必填的'})
        if employee.department_name != request.POST['department']:
            employee.department_name = request.POST['department']
            try:
                department = Department.objects.get(manager_id=employee.id)
                if department:
                    department.manager_id = None
                    department.manager_name = None
                    department.save()
            except Department.DoesNotExist:
                pass
        employee.save()
        return redirect('employee_info')
    return render(request, 'employee_edit.html', {'employee': employee})


@login_required
def employee_search(request):
    if request.method == "POST":
        user_id = request.POST['id']
        employee = get_object_or_404(Employee, id=user_id)
        return redirect('info_list', employee_id=employee.id)
    return render(request, 'employee_search.html')


@login_required
def info_list(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'info_list.html', {'employee': employee})


@login_required
def employee_info(request):
    employees = Employee.objects.all()
    return render(request, "employee_info.html", {'employees': employees})


@login_required
def department_info(request):
    departments = Department.objects.all()
    return render(request, "department_info.html", {'departments': departments})


@login_required
def department_add(request):
    if request.method == "POST":
        manager_id = request.POST['manager_id']
        manager_name = request.POST['manager']
        department_name = request.POST['department_name']
        description = request.POST['description']
        if not department_name or not manager_id or not manager_name:
            return render(request, 'department_add.html', {'error': '除了部门描述外其他字段必填'})
        department = Department(
            manager_id=manager_id,
            manager_name=manager_name,
            department_name=department_name,
            description=description,
        )
        department.save()
        return redirect('department_info')
    return render(request, 'department_add.html')


@login_required
def department_delete(request):
    if request.method == "POST":
        department_id = request.POST['id']
        department = get_object_or_404(Department, id=department_id)
        employees = Employee.objects.filter(department_name=department.department_name)
        if len(employees) > 0:
            employees.delete()
        else:
            pass
        department.delete()
        return redirect('department_info')
    return render(request, 'department_delete.html')


@login_required
def department_edit(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        department.manager_id = request.POST['manager_id']
        department.manager_name = request.POST['manager_name']
        department.department_name = request.POST['department_name']
        department.description = request.POST['description']
        if not department.manager_id or not department.manager_name or not department.department_name:
            return render(request, 'department_add.html', {'error': '除了部门描述外其他字段必填'})
        department.save()
        return redirect('department_info')
    return render(request, 'department_edit.html', {'department': department})


@login_required
def department_search(request):
    if request.method == "POST":
        department_id = request.POST['id']
        department = get_object_or_404(Department, id=department_id)
        return redirect('department_info_list', department_id=department.id)
    return render(request, 'department_search.html')


@login_required
def department_info_list(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    return render(request, 'department_info_list.html', {'department': department})


@login_required
def salary_info(request):
    salaries = Salary.objects.all()
    return render(request, "salary_info.html", {'salaries': salaries})


@login_required
def salary_add(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        employee_name = request.POST['employee_name']
        base_salary = request.POST['base_salary']
        bonus = request.POST['bonus']
        if not employee_id or not employee_name or not base_salary:
            return render(request, 'department_add.html', {'error': '除了奖金外其他字段必填'})
        total_salary = float(bonus) + float(base_salary)
        salary = Salary(
            employee_id=employee_id,
            name=employee_name,
            base_salary=base_salary,
            bonus=bonus,
            total_salary=total_salary
        )
        salary.save()
        try:
            employee = Employee.objects.get(id=employee_id)
            if employee:
                employee.total_salary = total_salary
                employee.save()
        except Employee.DoesNotExist:
            return render(request, 'salary_add.html', {'error': '员工不存在'})
        return redirect('salary_info')
    return render(request, 'salary_add.html')


@login_required
def salary_delete(request):
    if request.method == "POST":
        employee_id = request.POST['id']
        salaries = Salary.objects.filter(employee_id=employee_id)
        if len(salaries) > 0:
            salaries.delete()
        else:
            return render(request, 'salary_delete.html', {'error': '无薪资记录'})
        return redirect('salary_info')
    return render(request, 'salary_delete.html')


@login_required
def salary_search(request):
    if request.method == "POST":
        employee_id = request.POST['id']
        salaries = Salary.objects.filter(employee_id=employee_id)
        try:
            salary = salaries.first()
        except Salary.DoesNotExist:
            salary = None
        return redirect('salary_info_list', salary_employee_id=salary.employee_id)
    return render(request, 'salary_search.html')


@login_required
def salary_info_list(request, salary_employee_id):
    salaries = Salary.objects.filter(employee_id=salary_employee_id)
    return render(request, 'salary_info_list.html', {'salaries': salaries})


@login_required
def salary_edit(request, salary_id):
    salary = Salary.objects.get(id=salary_id)
    if request.method == "POST":
        salary.employee_id = request.POST['employee_id']
        salary.name = request.POST['employee_name']
        salary.base_salary = request.POST['base_salary']
        salary.bonus = request.POST['bonus']
        salary.total_salary = float(salary.base_salary) + float(salary.bonus)
        if not salary.base_salary or not salary.name or not salary.employee_id:
            return render(request, 'salary_edit.html', {'error': '有的字段不能为空'})
        salary.save()
        return redirect('salary_info')
    return render(request, 'salary_edit.html', {'salary': salary})


@login_required
def attendance_info(request):
    attendances = Attendance.objects.all()
    return render(request, "attendance_info.html", {'attendances': attendances})


@login_required
def attendance_add(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        name = request.POST['name']
        date = request.POST['date']
        attendance_status = request.POST['attendance_status']
        work_hours = request.POST['work_hours']
        if not employee_id or not name or not date or not attendance_status or not work_hours:
            return render(request, 'department_add.html', {'error': '有字段为空'})
        attendance = Attendance(
            employee_id=employee_id,
            name=name,
            date=date,
            attendance_status=attendance_status,
            work_hours=work_hours
        )
        attendance.save()
        return redirect('attendance_info')
    return render(request, 'attendance_add.html')


@login_required
def attendance_edit(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)
    if request.method == "POST":
        attendance.employee_id = request.POST['employee_id']
        attendance.name = request.POST['name']
        attendance.date = request.POST['date']
        attendance.attendance_status = request.POST['attendance_status']
        attendance.work_hours = request.POST['work_hours']
        if not attendance.employee_id or not attendance.name or not attendance.date or not attendance.attendance_status or not attendance.work_hours:
            return render(request, 'department_edit.html', {'error': '有字段为空'})
        attendance.save()
        return redirect('attendance_info')
    return render(request, 'attendance_edit.html', {'attendance': attendance})


@login_required
def attendance_search(request):
    if request.method == "POST":
        employee_id = request.POST['id']
        attendances = Attendance.objects.filter(employee_id=employee_id)
        try:
            attendance = attendances.first()
        except Attendance.DoesNotExist:
            attendance = None
        return redirect('attendance_info_list', attendanec_employee_id=attendance.employee_id)
    return render(request, 'attendance_search.html')


@login_required
def attendance_info_list(request, attendance_employee_id):
    attendances = Attendance.objects.filter(employee_id=attendance_employee_id)
    return render(request, 'attendance_info_list.html', {'attendances': attendances})


@login_required
def attendance_delete(request):
    if request.method == "POST":
        employee_id = request.POST['id']
        attendances = Attendance.objects.filter(employee_id=employee_id)
        if len(attendances) > 0:
            attendances.delete()
        else:
            return render(request, 'attendance_delete.html', {'error': '无出勤记录'})
        return redirect('attendance_info')
    return render(request, 'attendance_delete.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
