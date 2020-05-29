from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from djoser.conf import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from manage_student.api.serializers.serializers import ExUserSerializers
from manage_student.forms import AuthUserFrom
from manage_student.models import ExUser


# class ExUSerAPIView(APIView):
#     def post(self, request):
#         mydata = ExUserSerializers(data=request.data)
#         if not mydata.is_valid():
#             return Response('err ', status=status.HTTP_400_BAD_REQUEST)
#         elif mydata.username == User.username:
#             return Response('err ')
#         email = mydata.data['username']
#         password = mydata.data['password']
#         is_baned = mydata.data['remember_me']
#         ex = ExUser.objects.create(email=email, password=password,is_baned=is_baned)
#         return Response(data=ex.id, status=status.HTTP_200_OK)
# def login(request):
#     form_class = AuthUserFrom()
#     return render(request, 'manage_student/login.html', {'form_class': form_class})
#
#
def register(request):
    q =[]
    return render(request, 'manage_student/register.html')


@login_required(login_url='/account/login')
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'manage_student/index.html')
    else:
        pass


def logout_view(request):
    logout(request)
    return redirect('news:login')


class Login(LoginView):
    form_class = AuthUserFrom
    template_name = 'manage_student/login.html'

    def get(self, request, *args, **kwargs):
        if request.session.get_expiry_age() > 0:
            if request.user.is_authenticated:
                return redirect('news:dashboard')
            else:
                logout(request)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(0)
        return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def get_success_url(self):
        self.success_url = reverse_lazy('news:dashboard')
        return self.success_url
