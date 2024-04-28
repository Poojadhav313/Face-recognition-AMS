from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
    path('', views.home, name="home_page"),
    path('capture', views.capture, name="capture_page"),
    path('add', views.addData, name="adddata_page"),
    path('login', views.login, name="login_page"),
    ]