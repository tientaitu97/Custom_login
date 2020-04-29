from manage_student.models import StudentModel, SubjectsModel, ScoreModel
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
        st_list = StudentModel.objects.all()
        sb_list = SubjectsModel.objects.all()

        for _ in range(0, records):
            ScoreModel.objects.create(
                semester=random.choice(['Học Kì 1', 'Học Kì 2']),
                test_score=random.randrange(0, 11),
                subject_id=random.choice(sb_list),
                student_id=random.choice(st_list)
            )
