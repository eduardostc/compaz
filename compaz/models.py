from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Gerenciador de usuário personalizado
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        username = extra_fields.get('username', email)  # Usa o email como username, se não for fornecido
        extra_fields.setdefault('username', username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')
        
        return self._create_user(email, password, **extra_fields)

# Modelo de usuário personalizado
class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=False)

    local_servico = models.ForeignKey(
        'LocalServico',  # Referência ao modelo LocalServico
        on_delete=models.SET_NULL,  # Define o comportamento ao excluir o LocalServico
        null=True,  # Permite que o campo seja nulo
        blank=True,  # Permite que o campo seja deixado em branco no formulário
        verbose_name='Local do Serviço'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    
    objects = UsuarioManager()

# Modelos existentes da aplicação compaz
class LocalServico(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Area(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Atendimento(models.Model):
    atendente = models.ForeignKey(CustomUsuario, on_delete=models.CASCADE)  # Alterado para CustomUsuario
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
