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
    list_display = ('email', 'first_name', 'last_name', 'fone', 'is_staff', 'is_active', 'local_servico')
    
    # Campos que serão usados para filtrar a lista de usuários
    list_filter = ('is_staff', 'is_active', 'local_servico')
    
    # Campos que serão usados para buscar usuários
    search_fields = ('email', 'first_name', 'last_name')
    
    # Ordenação padrão da lista de usuários
    ordering = ('email',)
    
    # Campos que serão exibidos no formulário de edição de usuários
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone', 'local_servico')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos que serão exibidos no formulário de criação de usuários
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'fone', 'password1', 'password2', 'is_staff', 'is_active', 'local_servico'),
        }),
    )

# Registrar os outros modelos
admin.site.register(LocalServico)
admin.site.register(Area)
admin.site.register(Atendimento)

