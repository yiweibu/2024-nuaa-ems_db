from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
# Create your models here.


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


# 雇员模型
class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=128, unique=True, default='user@123.com')
    password = models.CharField(max_length=128, default='123456')
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    id = models.AutoField(primary_key=True, verbose_name='员工ID')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='性别')
    age = models.CharField(max_length=10, verbose_name='年龄', null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name='职位')
    department_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='部门')
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总薪资', blank=True, null=True)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='联系电话')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser


# 部门模型
class Department(models.Model):
    manager_id = models.IntegerField(null=True, blank=True, verbose_name='部门管理员ID')
    manager_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='部门管理员')
    department_name = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='部门')
    member_num = models.IntegerField(null=True, blank=True, verbose_name='部门人数')
    description = models.TextField(null=True, blank=True, verbose_name='部门描述')

    def __str__(self):
        return self.department_name


# 薪水模型
class Salary(models.Model):
    employee_id = models.IntegerField(null=True, blank=True, verbose_name='员工ID')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='姓名')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='奖金')
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总薪资')

    def __str__(self):
        return f"Salary record for employee"


class Attendance(models.Model):
    employee_id = models.IntegerField(null=True, blank=True, verbose_name='员工ID')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='姓名')
    date = models.DateField()
    attendance_status = models.CharField(max_length=50, choices=(
        ('Present', '正常'),
        ('Late', '迟到'),
        ('Early', '早退'),
        ('Absent', '请假'),
        # 更多出勤状态...
    ))
    work_hours = models.DecimalField(max_digits=5, decimal_places=2)
