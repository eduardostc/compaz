from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import BuscarServicosView


urlpatterns = [
    path('novo-atendimento/', views.novo_atendimento, name='novo_atendimento'),
    path('meus-atendimentos/', views.meus_atendimentos, name='meus_atendimentos'),

    path('atendimentos-unidade/', views.atendimento_unidade, name='atendimentos_unidade'),
    path('atendimentos-geral/', views.atendimento_geral, name='atendimentos_geral'),

    path('alterar_senha/', auth_views.PasswordChangeView.as_view(), name='alterar_senha'),
    path('alterar_senha/done/', auth_views.PasswordChangeDoneView.as_view(), name='alterar_senha_done'),

    
]

# https://www.youtube.com/watch?v=-ZK5eCyJIWo
# Aula 10: Alteração de Senha no Django!

# https://www.youtube.com/watch?v=gDRKwa1fzs4
# Aula 11: Recuperando o Controle - Reset de Senha no Django!

# https://www.youtube.com/watch?v=lVbozsNX9ow
# IMPLEMENTANDO "ESQUECI/RESETAR SENHA" (PYTHON/DJANGO)
