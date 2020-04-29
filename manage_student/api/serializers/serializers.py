from rest_framework import serializers
from manage_student.models import ExUser


class ExUserSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    remember_me = serializers.BooleanField(default=False)
