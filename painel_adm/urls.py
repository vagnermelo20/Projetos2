from django.contrib import admin
from django.urls import path, include
from painel_adm.views import InicioView,CriarCurso,EditarCurso,DeletarCurso,VisualizarCurso,VisualizarProcesso,EditarProcesso,DeletarProcesso,CriarProcessoSeletivo,VisualizarAlunos,PainelContas,EditarContas,DeletarContas,InicioProfessor,CriarContas,GerenciamentoAcad,VisualizarAlunosProf,AvaliacaoMetricas,AdicionarLote,RodarWpp,AceitarMatricula,VisualizarAlunosAdmin

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
    path('visualizar_alunos/<str:curso>/',VisualizarAlunos.as_view(),name='visualizar_alunos'),
    path('painel_contas/',PainelContas.as_view(),name='painel_contas'),
    path('editar_contas/<int:conta_id>/',EditarContas.as_view(),name="editar_contas"),
    path('deletar_contas/<int:conta_id>/',DeletarContas.as_view(),name="deletar_contas"),
    path('inicio_professor/<str:curso>/',InicioProfessor.as_view(),name="inicio_professor"),
    path('criar_contas/',CriarContas.as_view(),name='criar_contas'),
    path('gerenciamento_acad/<str:curso>/',GerenciamentoAcad.as_view(),name='gerenciamento_acad'),
    path('visualizar_alunos_prof/<str:curso>/',VisualizarAlunosProf.as_view(), name='visualizar_alunos_prof'),
    path('avaliacao_metricas/<str:nome_aluno>/<str:curso>/',AvaliacaoMetricas.as_view(),name='avaliacao_metricas'),
    path('adicionar_lotes/<str:nome>/',AdicionarLote.as_view(),name='adicionar_lote'),
    path('rodar_wpp/<str:curso>/',RodarWpp.as_view(),name="rodar_wpp"),
    path('aceitar_matricula/<str:curso>/',AceitarMatricula.as_view(),name="aceitar_matricula"),
    path('visualizar_alunos_curso/<str:curso>/',VisualizarAlunosAdmin.as_view(),name="visualizar_alunos_adm"),
    
]
