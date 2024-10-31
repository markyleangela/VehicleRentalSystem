# license/management/commands/generate_license_data.py
from django.core.management.base import BaseCommand
from license.models import License
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate dummy license numbers'

    def handle(self, *args, **kwargs):
        for _ in range(100):  # Adjust the number as needed
            license_number = f"G{random.randint(1, 99):02}-{random.randint(1, 99):02}-{random.randint(100000, 999999)}"
            expiration_date = datetime.today() + timedelta(days=random.randint(365, 3650))
            License.objects.create(
                license_number=license_number,
                licensee_name=f"Licensee {_}",
                expiration_date=expiration_date,
                status='active' if random.choice([True, False]) else 'inactive'
            )
        self.stdout.write(self.style.SUCCESS('Successfully created dummy license data'))
