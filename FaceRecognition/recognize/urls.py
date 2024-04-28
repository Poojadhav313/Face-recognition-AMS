from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
    path('', views.home, name="home_page"),
    path('capture', views.capture, name="capture_page"),
    path('adddata', views.addData, name="adddata_page"),
    path('login', views.login, name="login_page"),
    path('profile', views.profile, name="profile_page"),
    path('loginreq', views.loginReq, name="loginreq_page"),
    path('viewdata', views.viewData, name="viewdata_page"),
    
    ]