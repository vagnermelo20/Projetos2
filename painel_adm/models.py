from django.db import models

class Curso(models.Model):
    
    Nome = models.CharField(max_length=1000)
    Descrição = models.TextField()
    Numero_alunos=models.IntegerField()
    Numero_Professores=models.IntegerField()
    
    def __str__(self):
        return self.Nome

class Selecao(models.Model):
    data_inicio = models.DateField()
    data_fim = models.DateField()
    max_participantes = models.IntegerField()
    curso_para_processo=models.CharField(max_length=1000)

class Inscricao(models.Model):
    nome_inscrito=models.CharField(max_length=1000)
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
    nome_curso=models.CharField(max_length=300)
    
    def approve(self):
        self.status = 'aprovado'
        self.save()
        
    def reject(self):
        self.status = 'rejeitado'
        self.save()
    
