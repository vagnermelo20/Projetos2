from django.contrib import admin
from django.urls import path, include
from painel_adm.views import InicioView,CriarCurso,EditarCurso,DeletarCurso,VisualizarCurso

urlpatterns = [
    path('',InicioView.as_view(),name="inicio_painel"), 
    path('criar_curso/',CriarCurso.as_view(),name="criar_curso"),
    path('visualizar_Curso/',VisualizarCurso.as_view(),name="visualiar_curso"),
    path('editar_curso/',EditarCurso.as_view(),name="editar_curso"),
    path('deletar_curso/',DeletarCurso.as_view(),name="deletar_curso"),
    path('django-admin/', admin.site.urls),  # Renomeado para evitar conflito com suas rotas admin personalizadas
]