from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add/', views.addData),
    
    ]