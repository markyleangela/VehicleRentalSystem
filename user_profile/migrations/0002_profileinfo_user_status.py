# Generated by Django 5.1.1 on 2024-10-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileinfo',
            name='user_status',
            field=models.BooleanField(default=False),
        ),
    ]
