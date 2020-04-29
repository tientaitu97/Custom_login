from manage_student.models import StudentModel
from faker import Faker
from django.core.management.base import BaseCommand
import random

faker = Faker(['en-US', ])


class Command(BaseCommand):
    help = 'Faker data'

    def add_arguments(self, parser):
        parser.add_argument('records', type=int, help='Create records')

    def handle(self, *args, **options):
        records = options['records']

        for _ in range(0, records):
            StudentModel.objects.create(
                name_student=faker.name(),
                address=faker.address(),
                date=faker.date(),
                sex=random.choice(['Nam', 'Nữ'])
            )
