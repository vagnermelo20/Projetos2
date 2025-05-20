from django.db import models
from painel_adm.models import Curso
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    Username = models.CharField(max_length=100, unique=True)
    tipos_conta_escolha=[("Admin","Admin"),("Professor","Professor")]
    Tipos_conta=models.CharField(max_length=30,choices=tipos_conta_escolha,null=True, blank=True)
    E_mail = models.EmailField(unique=True)
    Senha = models.CharField(max_length=128)
    
    def save(self, *args, **kwargs):
        # Hash the password before saving to the database
        if self.Senha:
            self.Senha = make_password(self.Senha)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.Username
    


