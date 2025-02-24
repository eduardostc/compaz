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


#------------------------------------------antes da migração------------------------------------


# # core/urls.py (ou o caminho correto do seu arquivo urls.py)
# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views  # Importe as views de autenticação
# from compaz import views  # Importe suas views personalizadas, se necessário

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('login/', auth_views.LoginView.as_view(), name='login'),  # Use auth_views.LoginView
#     # path('signup/', views.signup, name='signup'),  # View de cadastro personalizada
#     path('', include('compaz.urls')),  # Inclua as URLs da aplicação compaz
# ]

# admin.site.site_header = 'Espaço Conecta'
# admin.site.site_title = 'Espaço Conecta'
# admin.site.index_title = 'Sistema de Gerenciamento do Espaço Conecta'