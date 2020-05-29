from manage_student.models import CourseModel
from faker import Faker
from django.core.management.base import BaseCommand
import random
from datetime import date, datetime

faker = Faker(['en-US', ])


def start_date(name):
    if name == "D13":
        return "2013-08-15"
    elif name == "D14":
        return "2014-08-15"
    elif name == "D15":
        return "2015-08-15"
    elif name == "D16":
        return "2016-08-15"
    elif name == "D17":
        return "2017-08-15"
    elif name == "D18":
        return "2018-08-15"
    elif name == "D19":
        return "2019-08-15"


def end_date(name):
    if name == 'D134':
        return "2017-08-15"
    elif name == 'D14':
        return "2018-08-15"
    elif name == 'D15':
        return "2019-08-15"
    elif name == 'D16':
        return "2020-08-15"
    elif name == 'D17':
        return "2021-08-15"
    elif name == 'D18':
        return "2022-08-15"
    elif name == 'D19':
        return "2023-08-15"


class Command(BaseCommand):
    help = 'Faker data'

    def add_arguments(self, parser):
        parser.add_argument('records', type=int, help='Create records')

    def handle(self, *args, **options):
        records = options['records']
        list_course = ['D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19']

        for i in range(0, records):
            CourseModel.objects.create(
                name_course=list_course[i],
                start_date=faker.date(),
                end_date=faker.date(),
            )
