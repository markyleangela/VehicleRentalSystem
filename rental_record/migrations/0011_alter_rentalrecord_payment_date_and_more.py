# Generated by Django 5.1.1 on 2024-11-30 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0010_alter_rentalrecord_rental_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalrecord',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rentalrecord',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rentalrecord',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
