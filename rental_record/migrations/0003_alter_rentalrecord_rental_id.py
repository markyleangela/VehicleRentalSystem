# Generated by Django 5.1.1 on 2024-10-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0002_remove_rentalrecord_id_rentalrecord_rental_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalrecord',
            name='rental_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
