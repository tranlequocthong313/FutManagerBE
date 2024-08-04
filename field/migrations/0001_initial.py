# Generated by Django 5.0.7 on 2024-08-03 20:06

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('img', cloudinary.models.CloudinaryField(max_length=255, null=True)),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('status', models.CharField(choices=[('available', 'Available'), ('booked', 'Booked'), ('under_maintenance', 'Under Maintenance')], default='available', max_length=20)),
                ('field_type', models.CharField(choices=[('5', '5-a-side'), ('7', '7-a-side'), ('11', '11-a-side')], default='5', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('from_time', models.DateTimeField()),
                ('to_time', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('booker_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('football_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field.field')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('available', 'Available'), ('booked', 'Booked'), ('under_maintenance', 'Under Maintenance')], max_length=20)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('football_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field.field')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
