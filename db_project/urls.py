"""
URL configuration for db_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  library import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin_view),
    path('signup/', views.signup_view),
    path('staff_menu/', views.staff_view),
    path('forgot_pwd/', views.forgot_pwd_view),
    path('user_menu/', views.user_menu_view),
    path('create_book/', views.create_book_view),
    path('user_management/', views.user_management_view),
    path('create_author/', views.create_author_view),
]