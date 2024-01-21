from django.contrib import admin
from django.urls import path
from phase3_server.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("other/", test_view),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("home/", home_view, name="home"),
    path("add_schedule/", add_schedule_view, name="add_schedule"),
    path("add_event/", add_event_view, name="add_event"),
    path('logout/', logout_view, name='logout'),
    path('other_action/', other_action_view, name='other_action'),
    path('user_views/', user_views, name='user_views')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)