from django.urls import path

from manage_student import views

app_name = 'news'
urlpatterns = [
    path('', views.register, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('demo/', views.demo, name='demo')
]
