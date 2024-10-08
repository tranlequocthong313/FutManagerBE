# Generated by Django 5.0.7 on 2024-08-05 03:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("field", "0007_rename_football_field_fieldstatushistory_field"),
        ("review", "0004_alter_review_football_field_alter_review_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="football_field",
            new_name="field",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="content",
            new_name="review",
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("user", "field")},
        ),
    ]
