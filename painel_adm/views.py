from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from painel_adm.models import Curso



class InicioView(View):
    def get(self, request):
        return render(request, 'painel_adm/inicio.html')
    

class CriarCurso(View):
    def get(self, request):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, "Você precisa estar logado para criar um curso.")
            return redirect('logar')

        # Renderiza o formulário de criação de objetivo
        return render(request, 'criar_curso.html')

    def post(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar um curso.")
            return redirect('logar')

        # Obter os dados do formulário
        nome_curso = request.POST.get('nome_curso')
        descricao_curso = request.POST.get('descricao')
        numero_alunos= request.POST.get('n_alunos')  
        numero_professores=request.POST.get('n_professores')

        # Validar o nome do objetivo
        if not nome_curso:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'painel_adm/criar_curso.html')

        # Verificar se já existe um objetivo com o mesmo nome para este usuário
        if Curso.objects.filter(Nome=nome_curso, usuario_id=usuario_id).exists():
            messages.error(request, 'Você já tem um curso com este nome.')
            return render(request, 'painel_adm/criar_curso.html', {
                'nome_curso': nome_curso,
                'descricao_curso': descricao_curso,
                'n_alunos':numero_alunos,
                'n_professores':numero_professores
            })


        # Criar o objetivo associado ao usuário logado
        Curso.objects.create(
            Nome=nome_curso,
            Descrição=descricao_curso,
            numero_alunos=numero_alunos,
            numero_professores=numero_professores
        )

        return redirect('visualizar_cursos')


class VisualizarCurso(View):
    def get(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar seu curso.")
            return redirect('logar')

        
        
        # Iniciar com todos os objetivos do usuário
        curso_query = Curso.objects.filter(usuario_id=usuario_id)
        
    
        cursos = curso_query

        context = {
            'cursos': cursos,
        }

        return render(request, 'painel_adm/visualizar_cursos.html', context)


class DeletarCurso(View):
    def post(self, request, curso_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para excluir seu curso.")
            return redirect('logar')

        # Buscar o objetivo e verificar se pertence ao usuário logado
        curso = get_object_or_404(Curso,id=curso_id)

        curso.delete()

        return redirect('visualizar_cursos.html')


class EditarCurso(View):
    def get(self, request, curso_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar objetivos.")
            return redirect('logar')

        curso = get_object_or_404(Curso, id=curso_id)

        context = {
            'curso': curso,
        }

        return render(request, 'painel_adm/editar_curso.html', context)

    def post(self, request, curso_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar objetivos.")
            return redirect('logar')

        curso = get_object_or_404(Curso, id=curso_id)

        nome_curso = request.POST.get('nome_curso')
        descricao_curso = request.POST.get('descricao_curso')
        numero_alunos= request.POST.get('n_alunos')  
        numero_professores=request.POST.get('n_professores')
        

        # Validar o nome do objetivo
        if not nome_curso:
            messages.error(request, 'É necessário preencher o nome do curso.')
            return render(request, 'objetivos/editar_objetivo.html', {'curso': curso})

        # Verificar se já existe OUTRO objetivo com o mesmo nome para este usuário
        # Usamos exclude(id=objetivo_id) para não considerar o próprio objetivo na verificação
        if Curso.objects.filter(Nome=nome_curso, usuario_id=usuario_id).exclude(id=curso_id).exists():
            messages.error(request, 'Você já tem um curso com este nome.')
            return render(request, 'objetivos/editar_objetivo.html', {
                'curso': curso,
                'nome_curso': nome_curso,
                'descricao_curso': descricao_curso,
                'n_alunos':numero_alunos,
                'n_professores':numero_professores
            })

        curso.Nome = nome_curso
        curso.Descrição = descricao_curso
        curso.Numero_alunos = numero_alunos
        curso.Numero_Professores=numero_professores
        curso.save()

        return redirect('visualizar_curso')