from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Usuario
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.template import RequestContext


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
                request.session['usuario_id'] = usuario.id
                request.session.save()  # Forçar a gravação da sessão
                # Redirecionar para a view de visualização de objetivos
                return redirect('painel_adm')
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return render(request, 'home/login.html')

class LogoutView(View):
    def get(self, request):
        # Remover o ID do usuário da sessão
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        
        return redirect('inicio') 
    
class InicioView(View):
    def get(self, request):
        return render(request, 'home/home.html')
