from django.db import models

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
        'Fundamental Incompleto','Fundamental Completo',
        'Médio Incompleto', 'Médio Completo',
        'Superior Incompleto', 'Superior Completo'
    ]
    Educacao = models.CharField(max_length=20, choices=EDUCACAO_ESCOLHA, null=True, blank=True)
    
    PERIODO_ESCOLHA = [
        'Manhã','Tarde','Noite','integral'
    ]
    Periodo_estudo = models.CharField(max_length=20, choices=PERIODO_ESCOLHA, null=True, blank=True)
    
    Curso_desejado = models.CharField(max_length=255, null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('rejeitado', 'Rejeitado')],
        default='pendente'
    )
    criado_a = models.DateTimeField(auto_now_add=True)
    
    def approve(self):
        self.status = 'aprovado'
        self.save()
        
    def reject(self):
        self.status = 'rejeitado'
        self.save()