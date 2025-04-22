from django.db import models

class Usuario(models.Model):
    Username = models.CharField(max_length=100, unique=True)
    E_mail = models.EmailField(unique=True)
    Senha = models.CharField(max_length=128)  

    def __str__(self):
        return self.Username

