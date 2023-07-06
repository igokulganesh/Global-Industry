from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),

    # For Login 
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logoutUser/',views.logoutUser,name='logoutUser'),
    path('profile/',views.profile,name='profile'),
    path('change_password/',views.change_password,name='change_password'),

]