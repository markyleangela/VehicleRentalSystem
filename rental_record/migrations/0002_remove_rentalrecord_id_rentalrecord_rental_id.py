# Generated by Django 5.1.1 on 2024-10-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalrecord',
            name='id',
        ),
        migrations.AddField(
            model_name='rentalrecord',
            name='rental_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
