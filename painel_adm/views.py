from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from painel_adm.models import Curso,Selecao,Inscricao

from home.models import Usuario




class InicioView(View):
    def get(self, request):
        return render(request, 'painel_adm/inicio.html')
    

class CriarCurso(View):
    def get(self, request):
        return render(request, 'painel_adm/criar_curso.html')

    def post(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
       
        # Obter os dados do formulário
        nome_curso = request.POST.get('nome_curso')
        descricao_curso = request.POST.get('descricao')
        numero_alunos= request.POST.get('n_alunos')  
        numero_professores=request.POST.get('n_professores')

       
        if not nome_curso or not descricao_curso or not numero_alunos or not numero_professores:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_curso.html')

        
        if Curso.objects.filter(Nome=nome_curso, id=usuario_id).exists():
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
            Numero_alunos=numero_alunos,
            Numero_Professores=numero_professores
        )

        return redirect('visualizar_curso')


class VisualizarCurso(View):
    def get(self, request):


        # usuario_id = request.session.get('usuario_id')
        
       
        curso_query = Curso.objects.all()
        
    
        cursos = curso_query

        context = {
            'cursos': cursos,
        }

        return render(request, 'painel_adm/visualizar_curso.html', context)


class DeletarCurso(View):
    def post(self, request, curso_id):
    
        curso = get_object_or_404(Curso,id=curso_id)

        curso.delete()

        return redirect('visualizar_curso')


class EditarCurso(View):
    def get(self, request, curso_id):
       
    
        curso = get_object_or_404(Curso, id=curso_id)

        context = {
            'curso': curso,
        }

        return render(request, 'painel_adm/editar_curso.html', context)

    def post(self, request, curso_id):
       
        usuario_id = request.session.get('usuario_id')
        curso = get_object_or_404(Curso, id=curso_id)

        nome_curso = request.POST.get('nome_curso')
        descricao_curso = request.POST.get('descricao_curso')
        numero_alunos= request.POST.get('n_alunos')  
        numero_professores=request.POST.get('n_professores')
        

       
        if not nome_curso or not descricao_curso or not numero_alunos or not numero_professores:
            messages.error(request, 'É necessário preencher todas as informações    .')
            return render(request, 'painel_adm/editar_curso.html', {'curso': curso})

        
        if Curso.objects.filter(Nome=nome_curso, id=usuario_id).exclude(id=curso_id).exists():
            messages.error(request, 'Você já tem um curso com este nome.')
            return render(request, 'painel_adm/editar_curso.html', {
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
        return render(request, 'painel_adm/criar_processo.html')

    def post(self, request):
       
        data_inicio= request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        max_participantes= request.POST.get('max_participantes')
        curso_para_processo= request.POST.get('curso_para_processo')

        if data_inicio >= data_fim:
            messages.error(request, 'A data de início não pode ser posterior ou igual à data final.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo': curso_para_processo
            })
        
        if not Curso.objects.filter(Nome=curso_para_processo).exists():
            messages.error(request,'Esse curso não existe') 
            return render(request, 'painel_adm/criar_processo.html', {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'max_participantes':max_participantes,
            'curso_para_processo':curso_para_processo
        })
        

        
        if not data_inicio or not data_fim or not max_participantes or not curso_para_processo:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_curso.html')

       
        if Selecao.objects.filter(curso_para_processo=curso_para_processo).exists():
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
    
        processo_query = Selecao.objects.all()
        
    
        selecao = processo_query

        context = {
            'selecao': selecao,
        }

        return render(request, 'painel_adm/visualizar_processo.html', context)
    
class DeletarProcesso(View):
    def post(self, request, processo_id):
        
        processo = get_object_or_404(Selecao, id=processo_id)

        processo.delete()

        return redirect('visualizar_processo')
    

class EditarProcesso(View):
    def get(self, request, processo_id):
       
        
        processo = get_object_or_404(Selecao, id=processo_id)

        context = {
            'processo': processo,
        }
        return render(request, 'painel_adm/editar_processo.html', context)

    def post(self, request, processo_id):
        processo = get_object_or_404(Selecao, id=processo_id)

        data_inicio= request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        max_participantes= request.POST.get('max_participantes')  
    
        

       
        if not data_inicio or not data_fim or not max_participantes:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/editar_processo.html', {'processo': processo})

        

        processo.data_inicio = data_inicio
        processo.data_fim = data_fim
        processo.max_participantes = max_participantes
        processo.save()

        return redirect('visualizar_processo')
    
class VisualizarAlunos(View):
    def get(self,request,curso):
        alunos = Inscricao.objects.filter(nome_curso=curso)
        context = {
            'alunos': alunos,
        }
        return render(request,'painel_adm/visualizar_alunos_processo.html',context)
    

class PainelContas(View):
    def get(self,request):
        conta=Usuario.objects.all()
        
        return render(request,'painel_adm/painel_contas.html',{'contas':conta})
    
class EditarContas(View):
    def get(self,request,conta_id):
        conta_edit=Usuario.objects.filter(id=conta_id)
        contexto={'conta':conta_edit}
        return render(request,'painel_adm/editar_contas.html',contexto)

    def post(self,request,conta_id):
        conta_edit=get_object_or_404(Usuario,id=conta_id)
        
        username=request.POST.get('username')
        email=request.POST.get('email')
        senha=request.POST.get('senha')
        

        if not username or not email or not senha:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/editar_contas.html', {'conta': conta_edit})
        
        conta_edit.Username=username
        conta_edit.E_mail=email
        conta_edit.Senha=senha
        conta_edit.save()
        return redirect('painel_contas')

class DeletarContas(View):
    def post(self,request,conta_id):
        conta_deletar=get_object_or_404(Usuario,id=conta_id)
        conta_deletar.delete()
        return redirect('painel_contas')

class InicioProfessor(View):
    def get(self,request):
        return render(request,"painel_adm/inicio_professor.html")
        
class CriarContas(View):
    
    def get(self,request):
        return render(request,"painel_adm/criar_contas.html")
    
    def post(self,request):

        nome_conta=request.POST.get('nome_conta')
        email=request.POST.get('email')
        senha=request.POST.get('senha')
        tipo_conta=request.POST.get('tipo_conta')
        curso_conta=request.POST.get('curso_conta')


        if not nome_conta or not email or not senha or not tipo_conta:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_contas.html')
        
        if tipo_conta=="Professor":
            if not curso_conta:
                messages.error(request,"É nescessário inserir o curso da conta para uma conta de professor")
                return render(request,'painel_adm/criar_contas.html')
            elif not Curso.objects.filter(Nome=curso_conta).exists():
                messages.error(request,"Esse curso não existe")
                return render(request,"painel_adm/criar_contas.html")
            else:
                Usuario.objects.create(
                    Username=nome_conta,
                    E_mail=email,
                    Senha=senha,
                    Tipos_conta=tipo_conta,
                    Curso=curso_conta,
                )
                messages.success(request,"Conta criada com sucesso")
                return redirect('painel_contas')
            
        
        
        if tipo_conta=="Administrador":
            Usuario.objects.create(
                Username=nome_conta,
                E_mail=email,
                Senha=senha,
                Tipos_conta=tipo_conta,
            )
            messages.success(request,"Conta criada com sucesso")
            return render(request,"painel_adm/criar_contas.html")

class GerenciamentoAcad(View):

    def get(self,request,curso):
        query_nomes=Inscricao.objects.filter(nome_curso=curso)
        contexto={'nomes':query_nomes,'curso':curso}
        return render(request,"painel_adm/gerenciamento_acad.html",contexto)
    
    def post(self,request,curso):
        total = int(request.POST.get("total_alunos", 0))
        for i in range(1, total + 1):
            aluno_id = request.POST.get(f"aluno_id_{i}")
            presenca = request.POST.get(f"presenca_{i}")
            if not presenca:
                messages.error(request,"É nescessários inserir a frequência de todos os estudantes.")
                return render(request,"painel_adm/gerenciamento_acad.html")

            if presenca=='faltou':
                aluno=get_object_or_404(Inscricao,id=aluno_id)
                aluno.quantidade_faltas+=1
                aluno.save()

        return render(request,"painel_adm/inicio_professor.html",{'curso':curso})

class VisualizarAlunosProf(View):

    def get(self,request,curso):
        query_nomes=Inscricao.objects.filter(nome_curso=curso)
        contexto={'nomes':query_nomes,'curso':curso}
        return render(request,"painel_adm/visualizar_alunos_prof.html",contexto)

class AvaliacaoMetricas(View):

    def get(self,request,nome_aluno):
        return render (request,'painel_adm/avaliacao_metricas.html')
    
    def post(self,request,nome_aluno):
        #criar model e terminar view
        return render(request,"painel_adm/gerenciamento_acad.html")
        
