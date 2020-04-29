from django import forms
from django.contrib.auth import authenticate
from rest_framework.exceptions import APIException

from manage_student.models import ExUser


class AuthUserFrom(forms.Form):
    email = forms.EmailField(label='Email', max_length=150,
                             widget=forms.TextInput(attrs={'autofocus': True, }),
                             error_messages={'invalid': 'Invalid email', 'required': 'Require email'})
    password = forms.CharField(label="Password", strip=False,
                               widget=forms.PasswordInput(
                                   attrs={}),
                               error_messages={'invalid': 'Invalid password', 'required': 'Require password'})
    remember_me = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    error_messages = {
        'invalid_login': "Email hoặc mật khẩu không chính xác",
        'inactive': "Tài khoản của bạn đã bị khoá!",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            try:
                self.user_cache = authenticate(self.request, email=email, password=password)
            except Exception as e:
                if isinstance(e, APIException):
                    pass
                else:
                    raise e
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': email})
            else:
                user = ExUser.objects.get(id=self.user_cache.id, is_active=1)
                if not user:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                        params={'email': self.email})

            return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
