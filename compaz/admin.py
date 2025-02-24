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



#--------------------------ou forma abaixo estar sem o modelo customizado de user---------------------------------------------------------------------------------------

# atendimento/admin.py

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, LocalServico, Area, Atendimento

# # Configuração personalizada para o modelo CustomUser no painel administrativo
# class CustomUserAdmin(UserAdmin):
#     # Campos que serão exibidos na lista de usuários
#     list_display = ('email', 'nome_completo', 'is_staff', 'is_active')
    
#     # Campos que serão usados para filtrar a lista de usuários
#     list_filter = ('is_staff', 'is_active')
    
#     # Campos que serão usados para buscar usuários
#     search_fields = ('email', 'nome_completo')
    
#     # Ordenação padrão da lista de usuários
#     ordering = ('email',)
    
#     # Campos que serão exibidos no formulário de edição de usuários
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Informações Pessoais', {'fields': ('nome_completo',)}),
#         ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
#     )
    
#     # Campos que serão exibidos no formulário de criação de usuários
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'nome_completo', 'password1', 'password2', 'is_staff', 'is_active'),
#         }),
#     )

# # Registrar o modelo CustomUser com a configuração personalizada
# admin.site.register(CustomUser, CustomUserAdmin)

# # Registrar os outros modelos
# admin.site.register(LocalServico)
# admin.site.register(Area)
# admin.site.register(Atendimento)