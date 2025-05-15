from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from home.models import Usuario,AlunoRegistro
from painel_adm.models import Inscricao,Selecao
from django.contrib.auth.hashers import make_password, check_password



class LoginView(View):
    def get(self, request):
        return render(request, 'home/login.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'home/login.html')

        try:
            usuario = Usuario.objects.get(E_mail=email)
            # Usar check_password para verificar a senha hasheada
            if check_password(senha, usuario.Senha):
                return redirect('inicio_painel')
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return render(request, 'home/login.html')

# class LogoutView(View):
#     def get(self, request):
#         # Remover o ID do usuário da sessão
#         if 'usuario_id' in request.session:
#             del request.session['usuario_id']
        
#         return redirect('inicio') 
    
class InicioView(View):
    def get(self, request):
        processo_query=Selecao.objects.all()
        processo=processo_query
        contexto={'processo':processo,}
        return render(request, 'home/home.html',contexto)


class Registrar_aluno(View):
    def get(self,request):
        return render(request, 'home/registro_aluno.html')

    def post(self,request):
    
        nome = request.POST.get('nome')
        telefone= request.POST.get('telefone')
        idade = request.POST.get('idade')
        bairro = request.POST.get('bairro')
        educacao = request.POST.get('educacao')
        periodo_estudo = request.POST.get('periodo_estudo')
        nome_do_processo=request.POST.get('nome_processo')
        
        

        if not nome or not telefone or not idade or not bairro or not educacao or not periodo_estudo:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'home/registro_aluno.html')

        if AlunoRegistro.objects.filter(Nome=nome).exists():
            messages.error(request, 'Candidato já registado.')
            return render(request, 'home/registro_aluno.html', {
            'nome': nome,
            'telefone': telefone,
            'idade':idade,
            'bairro':bairro,
            'educacao':educacao,
            'periodo_estudo':periodo_estudo,
        })
        elif AlunoRegistro.objects.filter(Telefone=telefone).exists():
            messages.error(request, 'Número já cadastrado. Insira outro número e tente novamente.')
            return render(request, 'home/registro_aluno.html', {
            'nome': nome,
            'telefone': telefone,
            'idade':idade,
            'bairro':bairro,
            'educacao':educacao,
            'periodo_estudo':periodo_estudo,
        })
        Inscricao.objects.create(
            nome_inscrito=nome,
            nome_curso=nome_do_processo,
        )
        try:
            AlunoRegistro.objects.create(
                Nome=nome,
                Telefone=telefone,
                Idade=idade,
                Bairro=bairro,
                Educacao=educacao,
                Periodo_estudo=periodo_estudo,
            )
            messages.success(request, 'O candidato foi registrado com sucesso!')
            return redirect('inicio')
        except:
            messages.success(request, 'Erro no registro do candidato!')
            return render(request,'home/registro_aluno.html')
        
class ProcessoView(View):
    def get(self, request):
        lista_processos=Selecao.objects.all()
        contexto={'processos':lista_processos}
        return render(request,'home/processos.html',contexto)
    
    
