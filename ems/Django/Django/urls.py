"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from ems import views
urlpatterns = [
    #path("admin/", admin.site.urls),
    path("",views.index,name='index'),
    path("login/",views.user_login,name='login'),
    path("logout/",views.user_logout,name='logout'),
    path("employee_info/",views.employee_info,name='employee_info'),
    path("employee_info/add/",views.employee_add,name='employee_add'),
    path("employee_info/delete/",views.employee_delete,name='employee_delete'),
    path("employee_info/<int:employee_id>/edit/",views.employee_edit,name='employee_edit'),
    path("employee_info/search/",views.employee_search,name='employee_search'),
    path("<int:employee_id>/info_list/",views.info_list,name='info_list'),
    path("department_info/",views.department_info,name='department_info'),
    path("department_info/add/",views.department_add,name='department_add'),
    path("department_info/delete/",views.department_delete,name='department_delete'),
    path("department_info/<int:department_id>/edit/",views.department_edit,name='department_edit'),
    path("department_info/search/",views.department_search,name='department_search'),
    path("<int:department_id>/department_info_list/", views.department_info_list, name='department_info_list'),
    path("salary_info/",views.salary_info,name='salary_info'),
    path("salary_info/add/",views.salary_add,name='salary_add'),
    path("salary_info/delete/",views.salary_delete,name='salary_delete'),
    path("salary_info/search/",views.salary_search,name='salary_search'),
    path("<int:salary_employee_id>/salary_info_list/", views.salary_info_list, name='salary_info_list'),
    path("salary_info/<int:salary_id>/edit/",views.salary_edit,name='salary_edit'),
    path("attendance_info/",views.attendance_info,name='attendance_info'),
    path("attendance_info/add/", views.attendance_add, name='attendance_add'),
    path("attendance_info/<int:attendance_id>/edit/", views.attendance_edit, name='attendance_edit'),
    path("attendance_info/search/", views.attendance_search, name='attendance_search'),
    path("<int:attendance_employee_id>/attendance_info_list/", views.attendance_info_list, name='attendance_info_list'),
    path("attendance_info/delete/",views.attendance_delete,name='attendance_delete'),
    path("admin_home/",views.admin_home,name='admin_home'),
    path("admin_home/<int:user_id>/edit/", views.admin_edit, name='admin_edit'),
    path("admin_home/<int:user_id>/change_admin_password/", views.change_admin_password, name='change_admin_password'),
    path("user_home/<int:user_id>/",views.user_home,name='user_home'),
    path("user_home/<int:user_id>/edit/", views.user_edit, name='user_edit'),
    path("user_home/<int:user_id>/change_user_password/", views.change_user_password, name='change_user_password')
]
