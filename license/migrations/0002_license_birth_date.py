# Generated by Django 5.1.1 on 2024-11-19 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
