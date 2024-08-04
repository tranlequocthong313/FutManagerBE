# Generated by Django 5.0.7 on 2024-08-04 07:39

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field', '0002_alter_booking_options_alter_field_options_and_more'),
        ('review', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_date'], 'verbose_name': 'Đánh giá', 'verbose_name_plural': 'Đánh giá'},
        ),
        migrations.AlterField(
            model_name='review',
            name='football_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field.field', verbose_name='Sân bóng'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=' Người nhận đánh giá'),
        ),
    ]
