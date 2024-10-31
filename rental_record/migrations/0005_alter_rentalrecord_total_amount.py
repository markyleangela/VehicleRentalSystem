# Generated by Django 5.1.1 on 2024-10-31 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0004_rentalrecord_days_rented'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalrecord',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
