# Generated by Django 5.0.7 on 2024-08-25 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("field", "0007_rename_football_field_fieldstatushistory_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fieldstatushistory",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
