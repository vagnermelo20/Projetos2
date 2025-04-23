from django.db import models

class Curso(models.Model):
    
    Nome = models.CharField(max_length=1000)
    Descrição = models.TextField()
    Numero_alunos=models.IntegerField()
    Numero_Professores=models.IntegerField()
    
    def __str__(self):
        return self.Nome

class Selecao(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    max_participantes = models.IntegerField()
    message_template = models.TextField()
    criado = models.DateTimeField(auto_now_add=True)
