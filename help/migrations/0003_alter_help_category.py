# Generated by Django 5.0.7 on 2024-08-04 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("help", "0002_alter_help_options_alter_helpcategory_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="help",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="help.helpcategory"
            ),
        ),
    ]
