import urllib.parse
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from painel_adm.models import Curso,Selecao,Inscricao,Lote
from .whatsapp import send_whatsapp_messages

from django.http import HttpResponse
import subprocess
import os
from home.models import Usuario
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



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

       
        if not nome_curso or not descricao_curso or not numero_alunos:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_curso.html')

        
        if Curso.objects.filter(Nome=nome_curso).exists():
            messages.error(request, 'Você já tem um curso com este nome.')
            return render(request, 'painel_adm/criar_curso.html', {
                'nome_curso': nome_curso,
                'descricao_curso': descricao_curso,
                'n_alunos':numero_alunos,
            })


        
        Curso.objects.create(
            Nome=nome_curso,
            Descrição=descricao_curso,
            Numero_alunos=numero_alunos,
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
 
        

       
        if not nome_curso or not descricao_curso or not numero_alunos:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/editar_curso.html', {'curso': curso})

        
        if Curso.objects.filter(Nome=nome_curso).exclude(id=curso_id).exists():
            messages.error(request, 'Você já tem um curso com este nome.')
            return render(request, 'painel_adm/editar_curso.html', {
                'curso': curso,
                'nome_curso': nome_curso,
                'descricao_curso': descricao_curso,
                'n_alunos':numero_alunos,
            })

        curso.Nome = nome_curso
        curso.Descrição = descricao_curso
        curso.Numero_alunos = numero_alunos
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
        data_inicio_aulas= request.POST.get('data_inicio_aulas')

        if date.fromisoformat(data_inicio) < date.today():
            messages.error(request, 'O processo seletivo não pode iniciar antes do dia de hoje.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo': curso_para_processo,
                'data_inicio_aulas': data_inicio_aulas,
            })
        
        if date.fromisoformat(data_inicio_aulas) < date.today() or date.fromisoformat(data_inicio_aulas) <date.fromisoformat(data_fim):
            messages.error(request, 'As aulas não podem começar hoje e devem iniciar após a data do fim informada.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo': curso_para_processo,
                'data_inicio_aulas':data_inicio_aulas,
            })
        
        

        um_ano_apos = date.today() + timedelta(days=366)
        if date.fromisoformat(data_inicio) > um_ano_apos:
            messages.error(request, 'A data de início deve estar no máximo até um ano a partir de hoje.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo': curso_para_processo,
                'data_inicio_aulas':data_inicio_aulas,
            })
        
        if (date.fromisoformat(data_fim) - date.fromisoformat(data_inicio)).days > 365:
            messages.error(request, 'O processo seletivo não pode durar mais de 1 ano.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo': curso_para_processo,
                'data_inicio_aulas':data_inicio_aulas,
            })


        if data_inicio >= data_fim:
            messages.error(request, 'A data de início não pode ser posterior ou igual à data final.')
            return render(request, 'painel_adm/criar_processo.html', {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'max_participantes': max_participantes,
                'curso_para_processo': curso_para_processo,
                'data_inicio_aulas':data_inicio_aulas,
            })
        
        if not Curso.objects.filter(Nome=curso_para_processo).exists():
            messages.error(request,'Esse curso não existe') 
            return render(request, 'painel_adm/criar_processo.html', {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'max_participantes':max_participantes,
            'curso_para_processo':curso_para_processo,
            'data_inicio_aulas':data_inicio_aulas,
        })
        

        
        if not data_inicio or not data_fim or not max_participantes or not curso_para_processo:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_curso.html')

    


        
        Selecao.objects.create(
            data_inicio=data_inicio,
            data_fim=data_fim,
            max_participantes=max_participantes,
            curso_para_processo=curso_para_processo,
            Data_inicio_aulas=data_inicio_aulas,
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
        return render(request, 'painel_adm/editar_processo.html', {'processo': processo})

    def post(self, request, processo_id):
        processo = get_object_or_404(Selecao, id=processo_id)

        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        max_participantes = request.POST.get('max_participantes')
        data_inicio_aulas = request.POST.get('data_inicio_aulas')

        context = {
            'processo': processo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'max_participantes': max_participantes,
            'data_inicio_aulas': data_inicio_aulas,
        }

        # Verificação de campos obrigatórios
        if not data_inicio or not data_fim or not max_participantes or not data_inicio_aulas:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/editar_processo.html', context)

        try:
            data_inicio_conv = date.fromisoformat(data_inicio)
            data_fim_conv = date.fromisoformat(data_fim)
            data_inicio_aulas_conv = date.fromisoformat(data_inicio_aulas)
        except ValueError:
            messages.error(request, 'Formato de data inválido.')
            return render(request, 'painel_adm/editar_processo.html', context)

        # Regras de negócio com datas
        if data_inicio_conv < date.today():
            messages.error(request, 'O processo seletivo não pode iniciar antes do dia de hoje.')
            return render(request, 'painel_adm/editar_processo.html', context)

        if data_inicio_aulas_conv < date.today() or data_inicio_aulas_conv < data_fim_conv:
            messages.error(request, 'As aulas não podem começar hoje e devem iniciar após a data do fim informada.')
            return render(request, 'painel_adm/editar_processo.html', context)

        if data_inicio_conv > date.today() + timedelta(days=366):
            messages.error(request, 'A data de início deve estar no máximo até um ano a partir de hoje.')
            return render(request, 'painel_adm/editar_processo.html', context)

        if (data_fim_conv - data_inicio_conv).days > 365:
            messages.error(request, 'O processo seletivo não pode durar mais de 1 ano.')
            return render(request, 'painel_adm/editar_processo.html', context)

        if data_inicio_conv >= data_fim_conv:
            messages.error(request, 'A data de início não pode ser posterior ou igual à data final.')
            return render(request, 'painel_adm/editar_processo.html', context)

        # Atualiza os dados permitidos
        processo.data_inicio = data_inicio
        processo.data_fim = data_fim
        processo.max_participantes = max_participantes
        processo.Data_inicio_aulas = data_inicio_aulas
        processo.save()

        return redirect('visualizar_processo')
    
    
class VisualizarAlunos(View):
    def get(self,request,curso):
        alunos = Inscricao.objects.filter(nome_curso=curso,aceito_em_lote="Não")
        query_lotes=Inscricao.objects.filter(nome_curso=curso,aceito_em_lote="Sim")
        query_entrevista=Inscricao.objects.filter(nome_curso=curso,em_entrevista="Sim")
        context = {
            'alunos': alunos,
            'aluno_lote':query_lotes,
            'aluno_entrevista':query_entrevista,
        }
        return render(request,'painel_adm/visualizar_alunos_processo.html',context)
    

class PainelContas(View):
    def get(self,request):
        conta=Usuario.objects.all()
        
        return render(request,'painel_adm/painel_contas.html',{'contas':conta})
    
class EditarContas(View): 
    def get(self, request, conta_id):
        conta_edit = get_object_or_404(Usuario, id=conta_id)
        contexto = {'conta': conta_edit, 'senha_visivel': '',}
        return render(request, 'painel_adm/editar_contas.html', contexto)

    def post(self, request, conta_id):
        conta_edit = get_object_or_404(Usuario, id=conta_id)
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not username or not email or not senha:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/editar_contas.html', {'conta': conta_edit})

        # Verificar se já existe outro usuário com esse username
        if Usuario.objects.filter(Username=username).exclude(id=conta_id).exists():
            messages.error(request, 'Já existe uma conta com esse nome de usuário.')
            return render(request, 'painel_adm/editar_contas.html', {'conta': conta_edit})

        # Verificar se já existe outro usuário com esse e-mail
        if Usuario.objects.filter(E_mail=email).exclude(id=conta_id).exists():
            messages.error(request, 'Já existe uma conta com esse e-mail.')
            return render(request, 'painel_adm/editar_contas.html', {'conta': conta_edit})

        conta_edit.Username = username
        conta_edit.E_mail = email
        conta_edit.Senha = senha  # será hasheada automaticamente no método save()
        conta_edit.save()

        messages.success(request, "Conta editada com sucesso.")
        return redirect('painel_contas')

    
class DeletarContas(View):
    def post(self,request,conta_id):
        conta_deletar=get_object_or_404(Usuario,id=conta_id)
        conta_deletar.delete()
        return redirect('painel_contas')

class InicioProfessor(View):
    def get(self,request,curso):
        return render(request,"painel_adm/inicio_professor.html",{'curso':curso})
        
class CriarContas(View):
    
    def get(self, request):
        return render(request, "painel_adm/criar_contas.html")
    
    def post(self, request):
        nome_conta = request.POST.get('nome_conta')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tipo_conta = request.POST.get('tipo_conta')
        curso_conta = request.POST.get('curso_conta')

        if not nome_conta or not email or not senha or not tipo_conta:
            messages.error(request, 'É necessário preencher todas as informações.')
            return render(request, 'painel_adm/criar_contas.html')

        # Verifica se já existe nome de usuário
        if Usuario.objects.filter(Username=nome_conta).exists():
            messages.error(request, 'Já existe uma conta com esse nome de usuário.')
            return render(request, 'painel_adm/criar_contas.html')

        # Verifica se já existe e-mail
        if Usuario.objects.filter(E_mail=email).exists():
            messages.error(request, 'Já existe uma conta com esse e-mail.')
            return render(request, 'painel_adm/criar_contas.html')

        if tipo_conta == "Professor":
            if not curso_conta:
                messages.error(request, "É necessário inserir o curso da conta para uma conta de professor.")
                return render(request, 'painel_adm/criar_contas.html')
            elif not Curso.objects.filter(Nome=curso_conta).exists():
                messages.error(request, "Esse curso não existe.")
                return render(request, "painel_adm/criar_contas.html")
            else:
                Usuario.objects.create(
                    Username=nome_conta,
                    E_mail=email,
                    Senha=senha,
                    Tipos_conta=tipo_conta,
                    Curso=curso_conta,
                )
                messages.success(request, "Conta criada com sucesso.")
                return redirect('painel_contas')

        if tipo_conta == "Administrador":
            Usuario.objects.create(
                Username=nome_conta,
                E_mail=email,
                Senha=senha,
                Tipos_conta=tipo_conta,
            )
            messages.success(request, "Conta criada com sucesso.")
            return redirect('painel_contas')

class GerenciamentoAcad(View):
    def get(self, request, curso):
        data_hoje = date.today()
        formatted_date = data_hoje.strftime("%d-%m-%Y")
        
        # QuerySet original de alunos para o curso
        query_nomes_qs = Inscricao.objects.filter(nome_curso=curso)

        data_avaliacoes_map = {}
        alunos_para_template = [] # Lista para os alunos com o atributo extra

        for aluno_obj in query_nomes_qs:
            # Calcula as datas de avaliação individuais para cada aluno
            datas_individuais = {
                'av1': aluno_obj.data_matricula,
                'av2': aluno_obj.data_matricula + relativedelta(months=1),
                'av3': aluno_obj.data_matricula + relativedelta(months=2),
            }
            data_avaliacoes_map[aluno_obj.id] = datas_individuais 

            # Adiciona as datas individuais de avaliação diretamente ao objeto aluno
            aluno_obj.data_av1 = datas_individuais['av1']
            aluno_obj.data_av2 = datas_individuais['av2']
            aluno_obj.data_av3 = datas_individuais['av3']

            # Adiciona o indicador se hoje é dia de avaliação (como já fizemos)
            aluno_obj.is_evaluation_day_today = (data_hoje == datas_individuais['av1'] or
                                                data_hoje == datas_individuais['av2'] or
                                                data_hoje == datas_individuais['av3'])
            alunos_para_template.append(aluno_obj)

        ja_enviou_hj_qs = Inscricao.objects.filter(
            data_envio=data_hoje, nome_curso=curso
        ).exists() 

        contexto = {
            'nomes': alunos_para_template, # Lista de alunos com 'is_evaluation_day_today'
            'curso': curso,
            'data': formatted_date,  
            'data_hoje': data_hoje,        # Objeto date para comparações no template 
            'data_avaliacoes': data_avaliacoes_map, 
            'ja_enviou_hj': ja_enviou_hj_qs, 
        }
        return render(request, "painel_adm/gerenciamento_acad.html", contexto)

    def post(self, request, curso):
        total_alunos_no_formulario = int(request.POST.get("quantidade_alunos", 0))
        data_hoje = date.today()

        if Inscricao.objects.filter(data_envio=data_hoje, nome_curso=curso).exists():
            messages.warning(request, f"Os dados de frequência para o curso {curso} já foram enviados hoje.")
            return redirect('inicio_professor', curso=curso) # Ou para 'gerenciamento_acad' com mensagem

        for i in range(1, total_alunos_no_formulario + 1):
            aluno_id = request.POST.get(f"aluno_id_{i}")
            presenca = request.POST.get(f"presenca_{i}")

            if not aluno_id: # Checagem extra, caso o ID do aluno não venha 
                messages.error(request, "Ocorreu um erro ao processar os dados de um aluno (ID não encontrado).")
             
                return redirect('gerenciamento_acad', curso=curso)


            if not presenca:
                # Erro: frequência não marcada para um aluno.
                # Recria o contexto como no método GET para re-renderizar o formulário.
                messages.error(request, "É necessário inserir a frequência (presente/faltou) de todos os estudantes.")

                query_nomes_qs_erro = Inscricao.objects.filter(nome_curso=curso)
                data_avaliacoes_reconstruido_erro = {}
                alunos_para_template_erro = []

                for aluno_obj_erro in query_nomes_qs_erro:
                    datas_individuais_erro = {
                        'av1': aluno_obj_erro.data_matricula,
                        'av2': aluno_obj_erro.data_matricula + relativedelta(months=1),
                        'av3': aluno_obj_erro.data_matricula + relativedelta(months=2),
                    }
                    data_avaliacoes_reconstruido_erro[aluno_obj_erro.id] = datas_individuais_erro
                    
                    aluno_obj_erro.is_evaluation_day_today = (data_hoje == datas_individuais_erro['av1'] or
                                                              data_hoje == datas_individuais_erro['av2'] or
                                                              data_hoje == datas_individuais_erro['av3'])
                    alunos_para_template_erro.append(aluno_obj_erro)
                

                ja_enviou_hj_qs_erro = Inscricao.objects.filter(
                    data_envio=data_hoje, nome_curso=curso
                ).exists()

                contexto_erro = {
                    'nomes': alunos_para_template_erro,
                    'curso': curso,
                    'data': data_hoje.strftime("%d-%m-%Y"),
                    'data_hoje': data_hoje,
                    'data_avaliacoes': data_avaliacoes_reconstruido_erro,
                    'ja_enviou_hj': ja_enviou_hj_qs_erro, 
                }
                return render(request, "painel_adm/gerenciamento_acad.html", contexto_erro)

            # Processa a presença do aluno
            aluno_instancia = get_object_or_404(Inscricao, id=aluno_id)
            if presenca == 'faltou':
                aluno_instancia.quantidade_faltas += 1
            
            aluno_instancia.data_envio = data_hoje # Marca que a presença deste aluno foi processada hoje
            aluno_instancia.save()

        # Se o loop completar sem erros para nenhum aluno
        messages.success(request, f"Frequência dos alunos do curso {curso} registrada com sucesso para {data_hoje.strftime('%d/%m/%Y')}!")
        return redirect('inicio_professor', curso=curso) 


class VisualizarAlunosProf(View):

    def get(self,request,curso):
        query_nomes=Inscricao.objects.filter(nome_curso=curso)
        contexto={'nomes':query_nomes,'curso':curso}
        return render(request,"painel_adm/visualizar_alunos_prof.html",contexto)

class AvaliacaoMetricas(View):
    def get(self, request, nome_aluno, curso):
        return render(request, 'painel_adm/avaliacao_metricas.html', {'curso': curso})

    def post(self, request, nome_aluno, curso):
        comunicacao = request.POST.get('comunicacao')
        conhecimento = request.POST.get('conhecimento')
        participacao = request.POST.get('participacao')

        if not comunicacao or not conhecimento or not participacao:
            messages.error(request, "É necessário inserir todas as informações.")
            # Passar nome_aluno para o contexto ao renderizar novamente
            return render(request, "painel_adm/avaliacao_metricas.html", {'curso': curso, 'nome_aluno': nome_aluno})

        aluno = get_object_or_404(Inscricao, nome_inscrito=nome_aluno, nome_curso=curso)
        nota_total = int(comunicacao) + int(conhecimento) + int(participacao)
        data_hoje = date.today()

        # Determinar as datas de avaliação específicas do aluno
        aluno_av1_date = aluno.data_matricula
        aluno_av2_date = aluno.data_matricula + relativedelta(months=1)
        aluno_av3_date = aluno.data_matricula + relativedelta(months=2)

        if data_hoje == aluno_av1_date:
            aluno.av1 = nota_total
        elif data_hoje == aluno_av2_date:
            aluno.av2 = nota_total
        elif data_hoje == aluno_av3_date:
            aluno.av3 = nota_total
        else:

            messages.error(request, f"Hoje ({data_hoje.strftime('%d/%m/%Y')}) não é uma data de avaliação válida para este aluno ou para a avaliação esperada.")
            return redirect('gerenciamento_acad', curso=curso)

        aluno.data_envio_avaliacao = data_hoje
        aluno.save()

        messages.success(request, "Avaliação registrada com sucesso!")
        return redirect('gerenciamento_acad', curso=curso)

class AdicionarLote(View):

    def get(self,request,nome):
        aluno=get_object_or_404(Inscricao,nome_inscrito=nome)
        processo=get_object_or_404(Selecao,curso_para_processo=aluno.nome_curso)
        aluno.aceito_em_lote="Sim"
        aluno.save()

        Lote.objects.create(
            nome_participante=nome,
            curso_do_lote=aluno.nome_curso,
        )
        query_entrevista=Inscricao.objects.filter(nome_curso=aluno.nome_curso,em_entrevista="Sim")
        alunos = Inscricao.objects.filter(nome_curso=aluno.nome_curso,aceito_em_lote="Não")
        query_lotes=Inscricao.objects.filter(nome_curso=aluno.nome_curso,aceito_em_lote="Sim")
        return render(request,"painel_adm/visualizar_alunos_processo.html",{'alunos':alunos,'aluno_lote':query_lotes,'aluno_entrevista':query_entrevista})


class RodarWpp(View):
    def post(self,request,curso):
        contacts=[]
        # Example values (in a real app, get these from request.GET or request.POST)
        aceitos_em_lote=Inscricao.objects.filter(nome_curso=curso, aceito_em_lote="Sim")
        for alunos in aceitos_em_lote:
            contacts.append(alunos.Telefone)
        message = request.POST.get('menssagem')

        send_whatsapp_messages(
            contacts=contacts,
            message=message,
        )
        for i in contacts:
            aluno=get_object_or_404(Inscricao,Telefone=i)
            aluno.em_entrevista="Sim"
            aluno.aceito_em_lote="N mais"
            aluno.save()

        query_entrevista=Inscricao.objects.filter(nome_curso=curso,em_entrevista="Sim")
        alunos = Inscricao.objects.filter(nome_curso=curso,aceito_em_lote="Não")
        query_lotes=Inscricao.objects.filter(nome_curso=curso,aceito_em_lote="Sim")
        return render(request,"painel_adm/visualizar_alunos_processo.html",{'alunos':alunos,'aluno_lote':query_lotes,'aluno_entrevista':query_entrevista})
    
class AceitarMatricula(View):

    def get(self,request,curso):

        query_em_entrevista=Inscricao.objects.filter(nome_curso=curso,em_entrevista="Sim")
        for aluno in query_em_entrevista:
            aluno.matriculado="Sim"
            aluno.em_entrevista="Não"
            aluno.save()

        alunos=Inscricao.objects.filter(nome_curso=curso,aceito_em_lote="Não")
        query_lotes=Inscricao.objects.filter(nome_curso=curso,aceito_em_lote="Sim")
        query_entrevista=Inscricao.objects.filter(nome_curso=curso,em_entrevista="Sim")
        messages.success(request,"Alunos cadastrados com sucesso")
        return render(request,"painel_adm/visualizar_alunos_processo.html",{"aluno":alunos,"aluno_lote":query_lotes,"aluno_entrevista":query_entrevista})

class VisualizarAlunosAdmin(View):

    def get(self,request,curso_id):

        curso=get_object_or_404(Curso,id=curso_id)
        alunos_query=Inscricao.objects.filter(nome_curso=curso.Nome, matriculado="Sim")
        return render(request,"painel_adm/visualizar_alunos_adm.html",{'alunos':alunos_query})
