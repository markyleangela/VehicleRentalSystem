# Generated by Django 5.1.1 on 2024-10-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_remove_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='license_no',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
