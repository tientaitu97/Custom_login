from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def create(self, validated_data):
        with transaction.atomic():
            user = super(UserRegistrationSerializer, self).create(validated_data)
            user.save()
            return user

    def validate(self, attrs):
        attrs = super(UserRegistrationSerializer, self).validate(attrs)
        request = self.context['request']
        if 'device_id' in request.data:
            attrs['device_id'] = request.data['device_id']
        else:
            raise exceptions.ValidationError(detail='Require device id')
        return attrs

    def to_representation(self, instance):
        data = super(UserRegistrationSerializer, self).to_representation(instance)
        data['device_id'] = instance.device_id
        refresh_token = self.get_token(instance)
        data['access'] = str(refresh_token.access_token)
        return data

