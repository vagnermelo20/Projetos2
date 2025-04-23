from django.contrib import admin
from django.urls import path, include
from home.views import InicioView,LoginView,AlunoRegistro,ProcessoView

urlpatterns = [
    path('',InicioView.as_view(), name='inicio'),
    path('login/',LoginView.as_view(), name='logar'),
    path('registro/',AlunoRegistro.as_views(),name='registro'),
    path('processos/',ProcessoView.as_view(),name='processo')
]