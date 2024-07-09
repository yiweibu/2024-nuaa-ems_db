# Generated by Django 4.1 on 2024-06-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ems", "0005_alter_employee_department_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="email",
            field=models.EmailField(
                default="user@123.com", max_length=128, unique=True
            ),
        ),
    ]