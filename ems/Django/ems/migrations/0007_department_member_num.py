# Generated by Django 4.1 on 2024-06-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ems", "0006_alter_employee_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="member_num",
            field=models.IntegerField(blank=True, null=True, verbose_name="部门人数"),
        ),
    ]