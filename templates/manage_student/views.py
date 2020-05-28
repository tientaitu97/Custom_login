from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy

from exuser.forms import AuthUserFrom


def register(request):
    return render(request, 'exuser/register.html')


@login_required(login_url='/account/login')
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'exuser/index.html')
    else:
        pass


def logout_view(request):
    logout(request)
    return redirect('exuser:login')


class Login(LoginView):
    form_class = AuthUserFrom
    template_name = 'exuser/login.html'

    def get(self, request, *args, **kwargs):
        if request.session.get_expiry_age() > 0:
            if request.user.is_authenticated:
                return redirect('exuser:dashboard')
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
        self.success_url = reverse_lazy('exuser:dashboard')
        return self.success_url
