from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
    path('capture/', views.temp, name="home"),
    path('add/', views.addData),
    
    ]