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
   
    
