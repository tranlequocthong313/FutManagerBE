# Generated by Django 5.0.7 on 2024-08-04 12:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("field", "0006_booking_paid_alter_booking_field_alter_booking_user_and_more"),
        ("review", "0003_alter_review_content_alter_review_unique_together"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="football_field",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="field.field"
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
