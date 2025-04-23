from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from painel_adm.models import Curso,Selecao



class InicioView(View):
    def get(self, request):
        return render(request, 'painel_adm/inicio.html')
    

class CriarCurso(View):
    def get(self, request):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, "Você precisa estar logado para criar um curso.")
            return redirect('logar')

       
        return render(request, 'painel_adm/criar_curso.html')

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

       
        if not nome_curso or not descricao_curso or not numero_alunos or not numero_professores:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_curso.html')

        
        if Curso.objects.filter(Nome=nome_curso, usuario_id=usuario_id).exists():
            messages.error(request, 'Você já tem um curso com este nome.')
            return render(request, 'painel_adm/criar_curso.html', {
                'nome_curso': nome_curso,
                'descricao_curso': descricao_curso,
                'n_alunos':numero_alunos,
                'n_professores':numero_professores
            })


        
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

        
        
       
        curso_query = Curso.objects.filter(usuario_id=usuario_id)
        
    
        cursos = curso_query

        context = {
            'cursos': cursos,
        }

        return render(request, 'painel_adm/visualizar_cursos.html', context)


class DeletarCurso(View):
    def post(self, request, curso_id):
        
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para excluir seu curso.")
            return redirect('logar')

        
        curso = get_object_or_404(Curso,id=curso_id)

        curso.delete()

        return redirect('visualizar_cursos.html')


class EditarCurso(View):
    def get(self, request, curso_id):
       
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar cursos.")
            return redirect('logar')

        curso = get_object_or_404(Curso, id=curso_id)

        context = {
            'curso': curso,
        }

        return render(request, 'painel_adm/editar_curso.html', context)

    def post(self, request, curso_id):
       
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar cursos.")
            return redirect('logar')

        curso = get_object_or_404(Curso, id=curso_id)

        nome_curso = request.POST.get('nome_curso')
        descricao_curso = request.POST.get('descricao_curso')
        numero_alunos= request.POST.get('n_alunos')  
        numero_professores=request.POST.get('n_professores')
        

       
        if not nome_curso:
            messages.error(request, 'É necessário preencher o nome do curso.')
            return render(request, 'objetivos/editar_objetivo.html', {'curso': curso})

        
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
    
class CriarProcessoSeletivo(View):
    def get(self, request):
        if 'usuario_id' not in request.session:
            messages.error(request, "Você precisa estar logado para criar um processo seletivo.")
            return redirect('logar')

        
        return render(request, 'painel_adm/criar_processo.html')

    def post(self, request):
       
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar um processo seletivo.")
            return redirect('logar')

        
        data_inicio= request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        max_participantes= request.POST.get('max_participantes')  
        curso_para_processo= request.POST.get('curso_para_proceso')
        if not Curso.objects.filter(Nome__iexact=curso_para_processo).exists():
            messages.error(request,'Esse curso não existe') 
            return render(request, 'home/registro_aluno.html', {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'max_participantes':max_participantes,
            'curso_para_processo':curso_para_processo
        })
        

        
        if not data_inicio or not data_fim or not max_participantes or not curso_para_processo:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_curso.html')

       
        if Curso.objects.filter(Nome=curso_para_processo).exists():
            messages.error(request, 'Você já tem um processo para esse curso.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes':max_participantes,
                'curso_para_processo':curso_para_processo
            })


        
        Selecao.objects.create(
            data_inicio=data_inicio,
            data_fim=data_fim,
            max_participantes=max_participantes,
            curso_para_processo=curso_para_processo
        )

        return redirect('visualizar_processo')
    

class VisualizarProcesso(View):
    def get(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar seu curso.")
            return redirect('logar')

       
        processo_query = Selecao.objects.filter(usuario_id=usuario_id)
        
    
        selecao = processo_query

        context = {
            'selecao': selecao,
        }

        return render(request, 'painel_adm/visualizar_processos.html', context)
    
class DeletarProcesso(View):
    def post(self, request, processo_id):
        
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para excluir seu curso.")
            return redirect('logar')

        
        curso = get_object_or_404(Curso,id=processo_id)

        curso.delete()

        return redirect('visualizar_processo')
    

class EditarProcesso(View):
    def get(self, request, processo_id):
       
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar cursos.")
            return redirect('logar')

        processo = get_object_or_404(Selecao, id=processo_id)

        context = {
            'processo': processo,
        }

        return render(request, 'painel_adm/editar_processo.html', context)

    def post(self, request, processo_id):
       
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar processos.")
            return redirect('logar')

        processo = get_object_or_404(Curso, id=processo_id)

        data_inicio= request.POST.get('data_inicio')
        data_fim = request.POST.get('descricao_curso')
        max_participantes= request.POST.get('max_participantes')  
        curso_para_processo=request.POST.get('curso_para_processo')
        

       
        if not data_inicio or not data_fim or not max_participantes or not curso_para_processo:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/editar_processo.html', {'processo': processo})

        
        if Curso.objects.filter(Nome=curso_para_processo, usuario_id=usuario_id).exclude(id=processo_id).exists():
            messages.error(request, 'Você já tem um processo para este curso.')
            return render(request, 'objetivos/editar_objetivo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo':curso_para_processo  
            })

        processo.data_inicio = data_inicio
        processo.data_fim = data_fim
        processo.max_participantes = max_participantes
        processo.curso_para_processo=curso_para_processo
        processo.save()

        return redirect('visualizar_processo')