from django.contrib import admin
from django.urls import path, include
from home.views import InicioView,LoginView,Registrar_aluno,ProcessoView
from . import views

urlpatterns = [
    path('',InicioView.as_view(), name='inicio'),
    path('login/',LoginView.as_view(), name='logar'),
    path('registro/', views.registro_aluno, name='registro_aluno'),
    path('processos/',ProcessoView.as_view(),name='processo'),
  
]