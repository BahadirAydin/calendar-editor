"""
URL configuration for client_phase3 project.

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
from phase3_server.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", connect_view),
    path("other/", test_view),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("home/", home_view, name="home"),
    path("add_schedule/", add_schedule_view, name="add_schedule"),
    path("add_event/", add_event_view, name="add_event"),
]
