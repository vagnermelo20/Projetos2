from django.contrib import admin
from django.urls import path, include
from painel_adm.views import InicioView,CriarCurso,EditarCurso,DeletarCurso,VisualizarCurso,VisualizarProcesso,EditarProcesso,DeletarProcesso,CriarProcessoSeletivo,VisualizarAplicantes

urlpatterns = [
    path('',InicioView.as_view(),name="inicio_painel"), 
    path('criar_curso/',CriarCurso.as_view(),name="criar_curso"),
    path('criar_processo',CriarProcessoSeletivo.as_view(),name="criar_processo"),
    path('visualizar_Curso/',VisualizarCurso.as_view(),name="visualizar_curso"),
    path('editar_curso/<int:curso_id>/',EditarCurso.as_view(),name="editar_curso"),
    path('deletar_curso/<int:curso_id>/',DeletarCurso.as_view(),name="deletar_curso"),
    path('editar_processo/<int:processo_id>/',EditarProcesso.as_view(),name="editar_processo"),
    path('deletar_processo/<int:processo_id>/',DeletarProcesso.as_view(),name="deletar_processo"),
    path('visualizar_processo/',VisualizarProcesso.as_view(),name="visualizar_processo"),
    path('visualizar_aplicantes/',VisualizarAplicantes.as_view(),name="visualizar_aplicantes"),
]
