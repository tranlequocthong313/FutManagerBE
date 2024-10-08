# Generated by Django 5.0.7 on 2024-08-25 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("field", "0008_alter_fieldstatushistory_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="status",
            field=models.CharField(
                choices=[("Available", "TRỐNG"), ("Maintenance", "ĐANG BẢO TRÌ")],
                default="Available",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="fieldstatushistory",
            name="status",
            field=models.CharField(
                choices=[("Available", "TRỐNG"), ("Maintenance", "ĐANG BẢO TRÌ")],
                max_length=20,
            ),
        ),
    ]
