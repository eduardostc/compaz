# atendimento/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# compaz/models.py
from django.contrib.auth.models import AbstractUser

class LocalServico(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Area(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Atendimento(models.Model):
    atendente = models.ForeignKey(User, on_delete=models.CASCADE)
    email_atendente = models.EmailField()
    data_atendimento = models.DateField(default=timezone.now)
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
    ]
    turno = models.CharField(max_length=5, choices=TURNO_CHOICES)
    local_servico = models.ForeignKey(LocalServico, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    nome_servico = models.CharField(max_length=255)
    nome_cidadao = models.CharField(max_length=120)
    telefone_cidadao = models.CharField(max_length=15)
    FORMA_ATENDIMENTO_CHOICES = [
        ('notebook', 'Notebook'),
        ('celular', 'Celular'),
        ('chat', 'Chat'),
    ]
    forma_atendimento = models.CharField(max_length=8, choices=FORMA_ATENDIMENTO_CHOICES)
    problema_resolvido = models.BooleanField()

    def __str__(self):
        return f"Atendimento {self.id} - {self.nome_cidadao}"
    

