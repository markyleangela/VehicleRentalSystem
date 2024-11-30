# Generated by Django 5.1.1 on 2024-11-30 05:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0012_rentalrecord_return_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalrecord',
            name='rental_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
