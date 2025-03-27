# compaz/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AtendimentoForm
from .models import Atendimento
from django.contrib.auth import login
#import para a funcionalidade do webhook
import requests
from django.contrib import messages
from django.utils import timezone
#imports responsável para aplicar o mes ao exibir os registro
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


############################## OS METODOS ABAIXO ESTÃO FUNCIONANDO PORÉM SEM EXIBIR OS REGISTRO POR MÊS #######################################
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

################FIM###################

# @login_required
# def novo_atendimento(request):
#     if request.method == 'POST':
#         form = AtendimentoForm(request.POST, user=request.user)  # Passa o usuário logado
#         if form.is_valid():
#             form.save()
#             return redirect('meus_atendimentos')
#     else:
#         form = AtendimentoForm(user=request.user)  # Passa o usuário logado
#         # Define o valor inicial do campo local_servico com base no usuário logado
#         if request.user.local_servico:
#             form.fields['local_servico'].initial = request.user.local_servico
#             form.fields['local_servico'].disabled = True  # Desabilita o campo se necessário

#         # Define o valor inicial do campo area com base no usuário logado
#         if request.user.area:
#             form.fields['area'].initial = request.user.area
#             form.fields['area'].disabled = True  # Desabilita o campo se necessário

#     return render(request, 'compaz/novo_atendimento.html', {'form': form})


WEBHOOK_URL = "https://webhook-n8n-dev-conectarecife.recife.pe.gov.br/webhook-test/compaz"
                

@login_required
def novo_atendimento(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, user=request.user)
        if form.is_valid():
            atendimento = form.save()
            
            # Prepara os dados para o webhook com os campos corretos
            dados_webhook = {
                'atendente': atendimento.atendente.get_full_name(),
                'email_atendente': atendimento.email_atendente,
                'data_atendimento': atendimento.data_atendimento.strftime('%Y-%m-%d'),
                'horario_atendimento': atendimento.horario_atendimento.strftime('%H:%M:%S'),
                'local_servico': str(atendimento.local_servico),
                'area': str(atendimento.area) if atendimento.area else '',
                'nome_servico': atendimento.nome_servico,
                'nome_cidadao': atendimento.nome_cidadao,
                'telefone_cidadao': atendimento.telefone_cidadao,
                'forma_atendimento': atendimento.forma_atendimento,
                'problema_resolvido': 'Sim' if atendimento.problema_resolvido else 'Não'
            }
            
            try:
                # print("Enviando dados para o webhook:", dados_webhook)  # Log para depuração
                response = requests.post(
                    WEBHOOK_URL,
                    json=dados_webhook,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                # print("Código de resposta do webhook:", response.status_code)
                # print("Resposta do webhook:", response.text)
                if response.status_code == 200:
                    messages.success(request, 'Atendimento registrado e enviado com sucesso!')
                else:
                    messages.warning(request, 'Atendimento registrado, mas houve um problema ao enviar para o sistema')
            except requests.exceptions.RequestException as e:
                messages.warning(request, f'Atendimento registrado, mas o sistema de integração está indisponível: {str(e)}')
            
            return redirect('meus_atendimentos')
    else:
        form = AtendimentoForm(user=request.user)
        if request.user.local_servico:
            form.fields['local_servico'].initial = request.user.local_servico
            form.fields['local_servico'].disabled = True
        if request.user.area:
            form.fields['area'].initial = request.user.area
            form.fields['area'].disabled = True

    return render(request, 'compaz/novo_atendimento.html', {'form': form})



#imports responsável pela API dos campos serviços
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
