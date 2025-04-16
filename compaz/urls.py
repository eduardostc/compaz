from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .views import excluir_atendimento, proxy_dashboard


urlpatterns = [
    # URL raiz redireciona para "Meus Atendimentos"
    path('', views.redirecionar_meus_atendimentos, name='raiz'),

    path('novo-atendimento/', views.novo_atendimento, name='novo_atendimento'),
    path('meus-atendimentos/', views.meus_atendimentos, name='meus_atendimentos'),
    path('atendimentos-unidade/', views.atendimento_unidade, name='atendimentos_unidade'),
    path('atendimentos-geral/', views.atendimento_geral, name='atendimentos_geral'),

   # Alteração de senha
    path('alterar_senha/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('alterar_senha_done')  # Redireciona para o nome da URL
    ), name='alterar_senha'),

    path('alterar_senha/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='alterar_senha_done'),

    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),
    #path('excluir-atendimento/<int:atendimento_id>/', excluir_atendimento, name='excluir_atendimento'),
    path('excluir-atendimento/<int:atendimento_id>/', views.excluir_atendimento, name='excluir_atendimento'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('proxy-dashboard/', proxy_dashboard, name='proxy_dashboard'),
]

# https://www.youtube.com/watch?v=-ZK5eCyJIWo
# Aula 10: Alteração de Senha no Django!

# https://www.youtube.com/watch?v=gDRKwa1fzs4
# Aula 11: Recuperando o Controle - Reset de Senha no Django!

# https://www.youtube.com/watch?v=lVbozsNX9ow
# IMPLEMENTANDO "ESQUECI/RESETAR SENHA" (PYTHON/DJANGO)
