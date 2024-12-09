import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from license.models import License
from faker import Faker

class Command(BaseCommand):
    help = "Generate dummy license data"

    def handle(self, *args, **kwargs):
        # Initialize Faker
        faker = Faker()

        # Generate 10 dummy licenses
        for _ in range(50):
            license_number = f"{random.choice('ABCDEFG')}{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}"
            birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
            licensee_name = faker.name()

            # Create and save the License object
            License.objects.create(
                license_number=license_number,
                licensee_name=licensee_name,
                expiration_date=timezone.now().date() + timezone.timedelta(days=random.randint(30, 365)),
                status=random.choice(['active', 'inactive']),
                birth_date=birth_date,
            )
        
        self.stdout.write(self.style.SUCCESS("Dummy data created successfully!"))
