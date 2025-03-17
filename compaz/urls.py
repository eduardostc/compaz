from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import BuscarServicosView


urlpatterns = [
    path('criar/', views.criar_atendimento, name='criar_atendimento'),
    path('listar/', views.lista_atendimentos, name='lista_atendimentos'),

    path('alterar_senha/', auth_views.PasswordChangeView.as_view(), name='alterar_senha'),
    path('alterar_senha/done/', auth_views.PasswordChangeDoneView.as_view(), name='alterar_senha_done'),
    # path("alterar-senha/", auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html"), name="alterar_senha"),
    # path("senha-alterada/", auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name="password_change_done"),
    # path('buscar-servicos/', BuscarServicosView.as_view(), name='buscar_servicos'),
]

# https://www.youtube.com/watch?v=-ZK5eCyJIWo
# Aula 10: Alteração de Senha no Django!

# https://www.youtube.com/watch?v=gDRKwa1fzs4
# Aula 11: Recuperando o Controle - Reset de Senha no Django!

# https://www.youtube.com/watch?v=lVbozsNX9ow
# IMPLEMENTANDO "ESQUECI/RESETAR SENHA" (PYTHON/DJANGO)
