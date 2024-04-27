from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
    path('', views.home, name="HOME"),
    path('capture/', views.capture, name="CAPTURE"),
    path('add/', views.addData, name="ADDDATA"),
    
    ]