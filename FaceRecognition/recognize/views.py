from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import *


def home(request):
    return render(request, "recognize/home.html")
