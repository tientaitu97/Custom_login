from django.contrib import admin
from .models import StudentModel, ScoreModel, SubjectsModel, ClassModel, CourseModel, FacultyModel, TrainingSystemModel
# Register your models here.
from manage_student.models import ExUser


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_student', 'address', 'sex', 'date']
    list_filter = ['name_student', 'sex']
    search_fields = ['name_student']


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_subjects', 'credit_number']
    list_filter = ['name_subjects', 'credit_number']
    search_fields = ['name_subjects']


class ScoreAdmin(admin.ModelAdmin):
    list_display = ['semester', 'test_score', 'subject_id', 'student_id']
    list_filter = ['test_score', 'semester']
    search_fields = ['semester']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_course', 'start_date', 'end_date']
    list_filter = ['name_course', 'start_date']
    search_fields = ['name_course']


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_faculty', 'address']
    list_filter = ['name_faculty', 'address']
    search_fields = ['name_faculty']


class TrainingSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_training']
    list_filter = ['name_training', 'id']
    search_fields = ['name_training']


class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_class', 'course_id', 'training_system_id', 'faculty_id']
    list_filter = ['name_class', 'id']
    search_fields = ['name_class']


admin.site.register(StudentModel, StudentAdmin)
admin.site.register(SubjectsModel, SubjectsAdmin)
admin.site.register(ScoreModel, ScoreAdmin)
admin.site.register(CourseModel, CourseAdmin)
admin.site.register(FacultyModel, FacultyAdmin)
admin.site.register(TrainingSystemModel, TrainingSystemAdmin)
admin.site.register(ClassModel, ClassAdmin)
admin.site.register(ExUser)