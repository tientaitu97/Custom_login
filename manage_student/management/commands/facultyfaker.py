from manage_student.models import FacultyModel
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
        list_faculty = ['Công ngệ thông tin', 'Điện tử', 'Viễn thông', ' Marketing', 'Kinh tế', 'Đa phương tiện']
        for i in range(0, records):
            FacultyModel.objects.create(
                name_faculty=list_faculty[i],
                address=faker.address(),
            )
