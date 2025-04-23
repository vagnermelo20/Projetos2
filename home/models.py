from django.db import models
from painel_adm.models import Curso

class Usuario(models.Model):
    Username = models.CharField(max_length=100, unique=True)
    E_mail = models.EmailField(unique=True)
    Senha = models.CharField(max_length=128)  

    def __str__(self):
        return self.Username

class AlunoRegistro(models.Model):
    Nome = models.CharField(max_length=255)
    Telefone = models.CharField(max_length=15)
    Idade = models.IntegerField(null=True, blank=True)
    Bairro = models.CharField(max_length=100, null=True, blank=True)
    
    EDUCACAO_ESCOLHA = [
        ('Fundamental Incompleto', 'Fundamental Incompleto'),
        ('Fundamental Completo', 'Fundamental Completo'),
        ('Médio Incompleto', 'Médio Incompleto'),
        ('Médio Completo', 'Médio Completo'),
        ('Superior Incompleto', 'Superior Incompleto'),
        ('Superior Completo', 'Superior Completo'),
    ]
    Educacao = models.CharField(max_length=23, choices=EDUCACAO_ESCOLHA, null=True, blank=True)
    
    PERIODO_ESCOLHA = [
        ('Manhã','Manhã'),('Tarde','Tarde'),('Noite','Noite'),('Integral','Integral')
    ]
    Periodo_estudo = models.CharField(max_length=20, choices=PERIODO_ESCOLHA, null=True, blank=True)
    
    
    ESCOLHA_STATUS=[('Pendente','Pendente'),('Aprovado','Aprovado'),('Rejeitado','Rejeitado')]
    
    status = models.CharField(
        max_length=20,
        choices=ESCOLHA_STATUS,
        default='Pendente'
    )
    criado_a = models.DateTimeField(auto_now_add=True)
    
    def approve(self):
        self.status = 'aprovado'
        self.save()
        
    def reject(self):
        self.status = 'rejeitado'
        self.save()