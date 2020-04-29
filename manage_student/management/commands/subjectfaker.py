from manage_student.models import SubjectsModel
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
        list_subject = ['Toán', 'Vật lí', 'Hóa học', ' Mác Lê-nin', 'Lập trình mạng','Lập trình web',
                    'Thống kê', ' Xác suất', 'Kinh tế vĩ mô', 'Hệ điều hành']
        for i in range(0, records):
            SubjectsModel.objects.create(
                name_subjects=list_subject[i],
                credit_number=random.randrange(1, 5),
            )