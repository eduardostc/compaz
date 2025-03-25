# compaz/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AtendimentoForm
from .models import Atendimento
from django.contrib.auth import login

import locale
from collections import defaultdict

# Configurar locale corretamente para exibir os registro por mês a mês no template
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # Fallback caso o sistema não tenha pt_BR.UTF-8

@login_required
def atendimento_geral(request):
    atendimentos = Atendimento.objects.all().order_by('-data_atendimento', '-horario_atendimento')

    # Agrupar atendimentos por mês
    atendimentos_por_mes = defaultdict(list)
    for atendimento in atendimentos:
        mes_ano = atendimento.data_atendimento.strftime('%B de %Y')
        mes_ano = mes_ano.encode('latin1').decode('utf-8').capitalize()  # Correção de encoding
        atendimentos_por_mes[mes_ano].append(atendimento)

    return render(request, 'compaz/atendimentos_geral.html', {'atendimentos_por_mes': dict(atendimentos_por_mes)})

@login_required
def meus_atendimentos(request):
    atendimentos = Atendimento.objects.filter(atendente=request.user).order_by('-data_atendimento', '-horario_atendimento')
    
    # Agrupar atendimentos por mês
    atendimentos_por_mes = defaultdict(list)
    for atendimento in atendimentos:
        mes_ano = atendimento.data_atendimento.strftime('%B de %Y')
        mes_ano = mes_ano.encode('latin1').decode('utf-8').capitalize()  # Correção de encoding
        atendimentos_por_mes[mes_ano].append(atendimento)
    
    return render(request, 'compaz/meus_atendimentos.html', {'atendimentos_por_mes': dict(atendimentos_por_mes)})

@login_required
def atendimento_unidade(request):
    # Obtém o local de serviço do usuário autenticado
    local_usuario = request.user.local_servico

    # Filtra os atendimentos pelo local do usuário autenticado
    atendimentos = Atendimento.objects.filter(local_servico=local_usuario).order_by('-data_atendimento', '-horario_atendimento')

    # Agrupar atendimentos por mês
    atendimentos_por_mes = defaultdict(list)
    for atendimento in atendimentos:
        mes_ano = atendimento.data_atendimento.strftime('%B de %Y')
        mes_ano = mes_ano.encode('latin1').decode('utf-8').capitalize()  # Correção de encoding
        atendimentos_por_mes[mes_ano].append(atendimento)

    return render(request, 'compaz/atendimentos_unidade.html', {'atendimentos_por_mes': dict(atendimentos_por_mes)})


############################## OS METODOS ABAIXO ESTÃO FUNCIONANDO PORÉM SEM EXIBIR POR MÊS #######################################
# @login_required
# def meus_atendimentos(request):
#     # atendimentos = Atendimento.objects.filter(atendente=request.user) #cada atendente só pode ver seus próprios atendimentos
#     atendimentos = Atendimento.objects.filter(atendente=request.user).order_by('-data_atendimento', '-horario_atendimento') #exibe os registros por ordem crescente.

#     #atendimentos = Atendimento.objects.all() #odos os usuários podem ver todos os atendimentos
#     return render(request, 'compaz/meus_atendimentos.html', {'atendimentos': atendimentos})


# @login_required
# def atendimento_unidade(request):
#     # Obtém o local de serviço do usuário autenticado
#     local_usuario = request.user.local_servico

#     # Filtra os atendimentos pelo local do usuário autenticado
#     atendimentos = Atendimento.objects.filter(local_servico=local_usuario).order_by('-data_atendimento', '-horario_atendimento')

#     return render(request, 'compaz/atendimentos_unidade.html', {'atendimentos': atendimentos})

# @login_required
# def atendimento_geral(request):
#     # Obtém todos os atendimentos sem filtros
#     atendimentos = Atendimento.objects.all().order_by('-data_atendimento', '-horario_atendimento')

#     return render(request, 'compaz/atendimentos_geral.html', {'atendimentos': atendimentos})



@login_required
def novo_atendimento(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, user=request.user)  # Passa o usuário logado
        if form.is_valid():
            form.save()
            return redirect('meus_atendimentos')
    else:
        form = AtendimentoForm(user=request.user)  # Passa o usuário logado
        # Define o valor inicial do campo local_servico com base no usuário logado
        if request.user.local_servico:
            form.fields['local_servico'].initial = request.user.local_servico
            form.fields['local_servico'].disabled = True  # Desabilita o campo se necessário

        # Define o valor inicial do campo area com base no usuário logado
        if request.user.area:
            form.fields['area'].initial = request.user.area
            form.fields['area'].disabled = True  # Desabilita o campo se necessário

    return render(request, 'compaz/novo_atendimento.html', {'form': form})


from django.http import JsonResponse
from django.views import View

class BuscarServicosView(View):
    def get(self, request, *args, **kwargs):
        termo = request.GET.get('termo', '')  # Termo digitado pelo usuário
        servicos = []  # Lista de serviços que será preenchida

        # Exemplo de busca em uma lista estática (substitua por uma busca no banco de dados)
        servicos_disponiveis = [
            "Serviço 1",
            "Serviço 2",
            "Serviço 3",
            "Outro Serviço",
        ]

        # Filtra os serviços que contêm o termo digitado
        servicos = [servico for servico in servicos_disponiveis if termo.lower() in servico.lower()]

        return JsonResponse(servicos, safe=False)
