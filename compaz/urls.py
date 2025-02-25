from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_atendimento, name='criar_atendimento'),
    path('listar/', views.lista_atendimentos, name='lista_atendimentos'),
]