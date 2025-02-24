Preciso fazer uma aplicação em django, o atendente irá precisar fazer a autenticação com usuário e senha. E quando acessar o sistema irá precisar preencher um formulário onde o esse formulário  ja deve vim preenchido automaticamente com os seguintes campos:
Nome do Atendente (preenchido automaticamente pelo nome do usuário no momento de cadastro da aplicação).
Email do atendente(preenchido automaticamente pelo nome do usuário no momento de cadastro da aplicação)..
Data do atendimento (a data atual).
Turno (Se o atendimento foi realizado no turno da manha ou no turno da tarde. Ou seja atendimentos das 6h até as 12h será prenchido automaticamente como manhã. E das 12h até as 18h será preenchido como tarde).
Local do serviço (terá as seguintes opções que será cadastrada pelo administrador: Compaz Ariano, Compaz Eduardo Campos; Compaz Dom Helder, Compaz ibura, Compaz atriz leda alves, unidade movel conecta, atendimento inss, Espaço conecta Metrô. Obs.: Mas será definido pelo administrador. ).
Area (Opção será cadastrada pelo administrador)
Nome do serviço (Esse campo de trazer ser uma lista dos serviços estão disponivel no url: https://carta-servicos-service.app.recife.pe.gov.br/cats/servicos?user_key=54db39aa505b40e86f020769a5d05097&quantidade=9999)
Nome do Cidadão (campo aberto com maximo de 120 caracteres)
Telefone do Cidadão (usar uma mascara de telefone)
Forma de atendimento (opções disponiveis: notebook, celular, chat)
Problema foi resolvido (opções disponivel: sim ou não).
Após preencher esse formulário deverá ter a opção do usuário acessar os atendimento que foram realizado por cada local do serviço (campo que será definido pelo administrador)
´´´´
você consegue me ajudar, visto que sou iniciante na area.

compaz/
├── __pycache__
├── migrations
├── templates/
    └── compaz/
	criar_atendimento.html
	lista_atendimento.html
    └── registration/
	login.html
	signup.html
└── __init__.py
└──admin.py
└──apps.py
└──forms.py
└──models.py
└──test.py
└──urls.py
└──views.py
core
├── asgipy
├── settings.py
├── urls.py
└── wsgi.py
venv
.gitignore
manage.py
db.sqlite3


*****************************************

Após migrar o sistema de autenticação da aplicação usuario para a aplicação compaz, utilizando o modelo CustomUsuario e seus formulários (CustomUsuarioCreateForm e CustomUsuarioChangeForm). Isso significa que o CustomUser da compaz será substituído pelo CustomUsuario da usuario.

O meu arquivo models.py ficou da seguinte forma:

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
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    def __str__(self):
        return self.email
    
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
´´´´
já o arquivo admin.py ficou da seguinte forma:

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsuario, LocalServico, Area, Atendimento
from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm

# Configuração personalizada para o modelo CustomUsuario no painel administrativo
@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario

    # Campos que serão exibidos na lista de usuários
    list_display = ('email', 'first_name', 'last_name', 'fone', 'is_staff', 'is_active')
    
    # Campos que serão usados para filtrar a lista de usuários
    list_filter = ('is_staff', 'is_active')
    
    # Campos que serão usados para buscar usuários
    search_fields = ('email', 'first_name', 'last_name')
    
    # Ordenação padrão da lista de usuários
    ordering = ('email',)
    
    # Campos que serão exibidos no formulário de edição de usuários
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos que serão exibidos no formulário de criação de usuários
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'fone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Registrar os outros modelos
admin.site.register(LocalServico)
admin.site.register(Area)
admin.site.register(Atendimento)
´´´´
quanto ao arquivo forms.py :

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Atendimento
from compaz.models import CustomUsuario  # Importa o modelo da app usuario
import requests
from datetime import datetime

class AtendimentoForm(forms.ModelForm):
    nome_servico = forms.ChoiceField(choices=[])  # Define o campo como ChoiceField
    forma_atendimento = forms.ChoiceField(
        choices=Atendimento.FORMA_ATENDIMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Atendimento
        fields = [
            'atendente', 'email_atendente', 'data_atendimento', 'turno',
            'local_servico', 'area', 'nome_servico', 'nome_cidadao',
            'telefone_cidadao', 'forma_atendimento', 'problema_resolvido'
        ]
        widgets = {
            'data_atendimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'},
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AtendimentoForm, self).__init__(*args, **kwargs)

        if user:
            self.initial['atendente'] = user.id
            self.fields['atendente'].disabled = True
            self.initial['email_atendente'] = user.email
            self.fields['email_atendente'].disabled = True
            self.initial['data_atendimento'] = datetime.now().date()
            self.fields['data_atendimento'].disabled = True

        # Definir turno automaticamente
        hora_atual = datetime.now().hour
        self.initial['turno'] = 'manha' if 6 <= hora_atual < 12 else 'tarde'
        self.fields['turno'].widget.attrs['disabled'] = 'disabled'

        # Buscar serviços da API
        try:
            response = requests.get('https://carta-servicos-service.app.recife.pe.gov.br/cats/servicos?user_key=54db39aa505b40e86f020769a5d05097&quantidade=9999')
            data = response.json()
            servicos = data.get("resposta", {}).get("dados", [])
            self.fields['nome_servico'].choices = [(servico["nome"], servico["nome"]) for servico in servicos]
        except Exception as e:
            print(f"Erro ao buscar serviços da API: {e}")
            self.fields['nome_servico'].choices = []

class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone', 'email')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')
´´´´
settings.py

# Redireciona para a página de criação de atendimento após o login
LOGIN_REDIRECT_URL = '/compaz/criar/'

# Modelo personalizado
AUTH_USER_MODEL = 'compaz.CustomUsuario'

´´´´
urls.py do projeto core

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importação das views de autenticação
from django.views.generic.base import RedirectView  # Para redirecionamentos
from compaz import views  # Suas views personalizadas

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs de autenticação do Django (login, logout, mudança de senha etc.)
    path('', include('django.contrib.auth.urls')),

    # Login e Logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Redirecionamento para login ao acessar a raiz do site
    path('', RedirectView.as_view(url='/login/')),

    # Inclui as URLs da aplicação compaz
    path('compaz/', include('compaz.urls')),
]

# Personalização do painel administrativo
admin.site.site_header = 'Espaço Conecta'
admin.site.site_title = 'Espaço Conecta'
admin.site.index_title = 'Sistema de Gerenciamento do Espaço Conecta'
´´´´
urls.py da app compaz

from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_atendimento, name='criar_atendimento'),
    path('lista/', views.lista_atendimentos, name='lista_atendimentos'),
]
´´´´
pasta templates
 subpasta
   Compaz: criar_atendimento.html
                   lista_atendimento.html
   registration:
                login.html
base.html
index.html
