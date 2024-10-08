# Generated by Django 5.0.7 on 2024-08-03 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('field', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('channel', models.CharField(choices=[('momo', 'Momo'), ('vn_pay', 'VNPay')], default='momo', max_length=20)),
                ('transaction_id', models.CharField(max_length=100)),
                ('reference_code', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field.booking')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
