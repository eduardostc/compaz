# compaz/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AtendimentoForm
from .models import Atendimento
from django.contrib.auth import login


@login_required
def lista_atendimentos(request):
    atendimentos = Atendimento.objects.filter(atendente=request.user) #cada atendente só pode ver seus próprios atendimentos
    #atendimentos = Atendimento.objects.all() #odos os usuários podem ver todos os atendimentos
    return render(request, 'compaz/lista_atendimentos.html', {'atendimentos': atendimentos})



@login_required
def criar_atendimento(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, user=request.user)  # Passa o usuário logado
        if form.is_valid():
            form.save()
            return redirect('lista_atendimentos')
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

    return render(request, 'compaz/criar_atendimento.html', {'form': form})


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
