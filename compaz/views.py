# compaz/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AtendimentoForm
from .models import Atendimento
#import para a funcionalidade do webhook
import requests
from django.contrib import messages
#imports responsável para aplicar o mes ao exibir os registro
import locale
from collections import defaultdict

#imports responsável para geracao do relatorio pdf.
from django.views import View
from django.http import FileResponse, HttpResponseForbidden
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io
from datetime import datetime

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib.auth.models import Group


class RelatorioView(View):
    def get(self, request, *args, **kwargs):
        # Verificar se o usuário pertence ao grupo "Gestores de Relatórios"
        is_gestor = request.user.groups.filter(name="Gestores de Relatórios").exists()
        #print("is_gestor:", is_gestor)  # Testa o valor no console

        if not is_gestor:
            return redirect('access_denied')  # Redireciona para uma página de acesso negado

        # Obtém o ano do parâmetro GET, padrão para o ano atual
        ano = request.GET.get("ano", datetime.now().year)

        # Verifica se o usuário quer baixar o PDF
        if "download" in request.GET:
            return self.gerar_pdf(ano)  # Passa o ano para o método gerar_pdf

        # Obtém os registros de Atendimento filtrando pelo ano
        atendimentos = Atendimento.objects.filter(data_atendimento__year=ano)

        # Mapeia os meses diretamente para português
        meses_nomes = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        atendimentos_por_local = {}

        for atendimento in atendimentos:
            local = atendimento.local_servico.nome
            mes_numero = atendimento.data_atendimento.month
            mes = meses_nomes[mes_numero - 1]

            if local not in atendimentos_por_local:
                atendimentos_por_local[local] = {m: 0 for m in meses_nomes}
            atendimentos_por_local[local][mes] += 1

        # Adiciona o total de atendimentos por local
        for local, meses_totais in atendimentos_por_local.items():
            meses_totais["Total"] = sum(meses_totais.values())

        # Criando a segunda tabela (dados por ano)
        anos_disponiveis = Atendimento.objects.dates("data_atendimento", "year")
        tabela_por_ano = []
        for ano_disponivel in anos_disponiveis:
            linha_ano = [ano_disponivel.year]  # Inicia a linha com o ano
            atendimentos_ano = Atendimento.objects.filter(data_atendimento__year=ano_disponivel.year)
            meses_totais = {mes: 0 for mes in meses_nomes}
            for atendimento in atendimentos_ano:
                mes_numero = atendimento.data_atendimento.month
                mes = meses_nomes[mes_numero - 1]
                meses_totais[mes] += 1
            linha_ano.extend([meses_totais[mes] for mes in meses_nomes])  # Adiciona os dados mensais
            tabela_por_ano.append(linha_ano)

        context = {
            "atendimentos_por_local": atendimentos_por_local,
            "meses_nomes": meses_nomes,
            "ano_selecionado": ano,
            "anos_disponiveis": anos_disponiveis,
            "tabela_por_ano": tabela_por_ano,  # Nova tabela
            "is_gestor": is_gestor,  # Variável adicionada ao contexto
        }

        # Renderiza o template HTML do relatório
        return render(request, "compaz/relatorio.html", context)

    def gerar_pdf(self, ano):
        """ Método separado para gerar e baixar o PDF """
        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

        # Estilo para o título
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos["Title"]

        # Criando o título para a primeira tabela
        titulo_principal = f"Relatório do Espaço Conecta do Ano - {ano}"
        elemento_titulo_principal = Paragraph(titulo_principal, estilo_titulo)

        # Adicionando espaço após o título
        espaçamento = Spacer(1, 20)

        # Cabeçalho da primeira tabela (por local)
        meses_nomes = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        tabela_dados = [["Local do Serviço"] + meses_nomes + ["Total"]]

        atendimentos = Atendimento.objects.filter(data_atendimento__year=ano)
        atendimentos_por_local = {}

        for atendimento in atendimentos:
            local = atendimento.local_servico.nome
            mes = meses_nomes[atendimento.data_atendimento.month - 1]

            if local not in atendimentos_por_local:
                atendimentos_por_local[local] = {m: 0 for m in meses_nomes}
            atendimentos_por_local[local][mes] += 1

        for local, meses_totais in atendimentos_por_local.items():
            meses_totais["Total"] = sum(meses_totais[m] for m in meses_nomes)
            linha = [local] + [meses_totais[m] for m in meses_nomes] + [meses_totais["Total"]]
            tabela_dados.append(linha)

        totais_por_mes = {m: sum(meses_totais[m] for meses_totais in atendimentos_por_local.values()) for m in meses_nomes}
        total_geral = sum(meses_totais["Total"] for meses_totais in atendimentos_por_local.values())
        tabela_dados.append(["Total"] + [totais_por_mes[m] for m in meses_nomes] + [total_geral])

        tabela_local = Table(tabela_dados)
        tabela_local.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))

        # Criando o título para a segunda tabela
        titulo_global = f"Relatório do Espaço Conecta Global"
        elemento_titulo_global = Paragraph(titulo_global, estilo_titulo)

        # Criando a segunda tabela (dados por ano)
        anos_disponiveis = Atendimento.objects.dates("data_atendimento", "year")
        tabela_por_ano = [["Ano"] + meses_nomes]
        for ano_disponivel in anos_disponiveis:
            linha_ano = [ano_disponivel.year]
            atendimentos_ano = Atendimento.objects.filter(data_atendimento__year=ano_disponivel.year)
            meses_totais = {mes: 0 for mes in meses_nomes}
            for atendimento in atendimentos_ano:
                mes_numero = atendimento.data_atendimento.month
                mes = meses_nomes[mes_numero - 1]
                meses_totais[mes] += 1
            linha_ano.extend([meses_totais[mes] for mes in meses_nomes])
            tabela_por_ano.append(linha_ano)

        tabela_anos = Table(tabela_por_ano)
        tabela_anos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Atualizando a ordem dos elementos
        elementos = [
            elemento_titulo_global,  # Adiciona o título da segunda tabela primeiro
            Spacer(1, 10),           # Espaço entre título e tabela
            tabela_anos,             # Adiciona a segunda tabela
            Spacer(1, 20),           # Espaço entre tabelas
            elemento_titulo_principal,  # Adiciona o título da primeira tabela
            espaçamento,
            tabela_local             # Adiciona a primeira tabela
        ]

        # Construindo o documento
        pdf.build(elementos)
        buffer.seek(0)

        return FileResponse(buffer, filename=f"relatorio_{ano}.pdf") 


# Configurar locale corretamente para exibir os registro por mês a mês no template
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # Fallback caso o sistema não tenha pt_BR.UTF-8

# @login_required
# def atendimento_geral(request):

#     atendimentos = Atendimento.objects.all().order_by('-data_atendimento', '-horario_atendimento')

#     # Agrupar atendimentos por mês
#     atendimentos_por_mes = defaultdict(list)
#     for atendimento in atendimentos:
#         mes_ano = atendimento.data_atendimento.strftime('%B de %Y')
#         mes_ano = mes_ano.encode('latin1').decode('utf-8').capitalize()  # Correção de encoding
#         atendimentos_por_mes[mes_ano].append(atendimento)

#     return render(request, 'compaz/atendimentos_geral.html', {'atendimentos_por_mes': dict(atendimentos_por_mes)})
    
@login_required
def atendimento_geral(request):
    atendimentos = Atendimento.objects.all().order_by('-data_atendimento', '-horario_atendimento')

    # Verificar se o usuário pertence ao grupo "Gerentes de Atendimento"
    is_gerente = request.user.groups.filter(name="Gerentes de Atendimento").exists()
    
    #print("is_gerente:", is_gerente)  # Testa o valor no console

    if not is_gerente:
        return redirect('access_denied')  # Redireciona para uma página de acesso negado

    # Agrupar atendimentos por mês
    atendimentos_por_mes = defaultdict(list)
    for atendimento in atendimentos:
        mes_ano = atendimento.data_atendimento.strftime('%B de %Y')
        mes_ano = mes_ano.encode('latin1').decode('utf-8').capitalize()  # Correção de encoding
        atendimentos_por_mes[mes_ano].append(atendimento)

    return render(request, 'compaz/atendimentos_geral.html', {
        'atendimentos_por_mes': dict(atendimentos_por_mes),
        'is_gerente': is_gerente  # Passa a variável para o template
    })


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


# WEBHOOK_URL = "https://webhook-n8n-dev-conectarecife.recife.pe.gov.br/webhook-test/compaz"
WEBHOOK_URL = "https://webhook-n8n-dev-conectarecife.recife.pe.gov.br/webhook-test/espaconecta" #tenorio
                

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
    

@login_required
def redirecionar_meus_atendimentos(request):
    # Redireciona para a página "Meus Atendimentos" se autenticado
    return redirect('meus_atendimentos')


@login_required
def excluir_atendimento(request, atendimento_id):
    """
    Exclui um atendimento específico, permitido apenas para membros do Grupo de Exclusão.
    """
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)

    # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
    pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

    if not pertence_grupo_exclusao:
        return HttpResponseForbidden("Você não tem permissão para excluir este atendimento.")

    if request.method == 'POST':
        # Exclui o atendimento
        atendimento.delete()
        messages.success(request, "Atendimento excluído com sucesso.")
        #return redirect('meus_atendimentos')  # Redireciona para o template de atendimentos
        
        # Verifica se há um parâmetro `next` na requisição
        next_url = request.GET.get('next', 'meus_atendimentos')  # Padrão: meus_atendimentos
        return redirect(next_url)  # Redireciona para a página de origem ou padrão

    # Renderiza os templates com o botão de exclusão visível somente para o grupo
    context = {
        'atendimento': atendimento,
        'pertence_grupo_exclusao': pertence_grupo_exclusao,
    }
    return render(request, 'compaz/meus_atendimentos.html', context)



