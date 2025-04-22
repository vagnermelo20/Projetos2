from django.contrib import admin
from django.urls import path, include
from home.views import InicioView,LoginView

urlpatterns = [
    path('',InicioView.as_view(), name='inicio'),
    path('login/',LoginView.as_view(), name='logar'),
]