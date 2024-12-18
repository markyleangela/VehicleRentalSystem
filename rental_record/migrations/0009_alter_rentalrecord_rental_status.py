# Generated by Django 5.1.1 on 2024-11-30 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0008_remove_rentalrecord_return_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalrecord',
            name='rental_status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Booked', 'Booked'), ('In Use', 'In_use'), ('Returned', 'Returned'), ('Overdue Pending', 'Overdue_pending'), ('Overdue Returned', 'Overdue_returned'), ('Overdue Extended', 'Overdue_extended'), ('Completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
