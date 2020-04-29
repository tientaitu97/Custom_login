import random

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import manage_student.constants as _const


class MyExUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        color = random.choice(_const.AVA_COLORS)
        return self._create_user(email, username, password, color_avatar=color, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        color = random.choice(_const.AVA_COLORS)
        return self._create_user(username, email, password, color_avatar=color, **extra_fields)


# Create your user models here.

class ExUser(AbstractUser):
    email = models.EmailField(blank=True, null=True, max_length=255, unique=True)
    password = models.CharField(blank=True, null=True, max_length=255, unique=True)
    username = models.CharField(blank=True, null=True, max_length=255, unique=False)
    color_avatar = models.CharField(blank=True, null=True, max_length=255, unique=False)
    device_id = models.CharField(blank=True, null=True, max_length=255)
    is_baned = models.BooleanField(default=False)

    objects = MyExUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'tbl_exuser'

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


class UserProfile(models.Model):
    GENDERS = (
        (_const.OTHER, _const.OTHER),
        (_const.MALE, _const.MALE),
        (_const.FEMALE, _const.FEMALE)
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='uploads', blank=True)
    gender = models.CharField(max_length=20, choices=GENDERS, default=_const.OTHER)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'tbl_user_profile'


class StudentModel(models.Model):
    name_student = models.CharField(max_length=255, null=True, blank=True, unique=False)
    sex = models.CharField(max_length=255, null=True, blank=True, unique=False)
    date = models.CharField(max_length=255, null=True, blank=True, unique=False)
    address = models.CharField(max_length=255, null=True, blank=True, unique=False)

    class Meta:
        db_table = 'Student'
        verbose_name = 'Student'

    def __str__(self):
        return self.name_student


class SubjectsModel(models.Model):
    name_subjects = models.CharField(max_length=255, null=True, blank=True, unique=False)

    credit_number = models.IntegerField(default=1)

    def __str__(self):
        return self.name_subjects

    class Meta:
        db_table = 'Subjects'
        verbose_name = 'Subjects'


class ScoreModel(models.Model):
    semester = models.CharField(max_length=255, null=True, blank=True, unique=False)
    test_score = models.IntegerField(default=0)
    subject_id = models.ForeignKey(SubjectsModel, null=True, blank=True, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(StudentModel, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Score'
        verbose_name = 'Score'


class CourseModel(models.Model):
    name_course = models.CharField(max_length=255, null=True, blank=True, unique=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name_course

    class Meta:
        db_table = 'Course'
        verbose_name = 'Course'


class TrainingSystemModel(models.Model):
    name_training = models.CharField(max_length=255, null=True, blank=True, unique=False)

    class Meta:
        db_table = 'TrainingSystem'
        verbose_name = 'TrainingSystem'

    def __str__(self):
        return self.name_training


class FacultyModel(models.Model):
    name_faculty = models.CharField(max_length=255, null=True, blank=True, unique=False)
    address = models.CharField(max_length=255, null=True, blank=True, unique=False)

    class Meta:
        db_table = 'Faculty'
        verbose_name = 'Faculty'

    def __str__(self):
        return self.name_faculty


class ClassModel(models.Model):
    name_class = models.CharField(max_length=255, null=True, blank=True, unique=False)
    course_id = models.ForeignKey(CourseModel, null=True, blank=True, on_delete=models.DO_NOTHING)
    training_system_id = models.ForeignKey(TrainingSystemModel, null=True, blank=True, on_delete=models.DO_NOTHING)
    faculty_id = models.ForeignKey(FacultyModel, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Class'
        verbose_name = 'Class'

    def __str__(self):
        return self.name_class
