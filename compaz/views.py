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

#imports responsável para geracao do relatorio pdf.
from django.shortcuts import render
from django.views import View
from django.http import FileResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io
from datetime import datetime
from .models import Atendimento

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class RelatorioView(View):
    def get(self, request, *args, **kwargs):
        # Obtém o ano do parâmetro GET, padrão para o ano atual
        ano = request.GET.get("ano", datetime.now().year)

        # Verifica se o usuário quer baixar o PDF
        if "download" in request.GET:
            return self.gerar_pdf(ano) # Passa o ano para o método gerar_pdf

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

        # Prepara o contexto para o template
        anos_disponiveis = Atendimento.objects.dates("data_atendimento", "year")
        context = {
            "atendimentos_por_local": atendimentos_por_local,
            "meses_nomes": meses_nomes,
            "ano_selecionado": ano,
            "anos_disponiveis": anos_disponiveis,
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

        # Criando o título
        titulo = f"Relatório do Espaço Conecta do Ano - {ano}"
        elemento_titulo = Paragraph(titulo, estilo_titulo)

        # Adicionando espaço após o título
        espaçamento = Spacer(1, 20)

        # Cabeçalho da tabela
        meses_nomes = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        tabela_dados = [["Local do Serviço"] + meses_nomes + ["Total"]]

        # Obtendo atendimentos agrupados pelo ano selecionado
        atendimentos = Atendimento.objects.filter(data_atendimento__year=ano)
        atendimentos_por_local = {}

        for atendimento in atendimentos:
            local = atendimento.local_servico.nome
            mes = meses_nomes[atendimento.data_atendimento.month - 1]

            if local not in atendimentos_por_local:
                atendimentos_por_local[local] = {m: 0 for m in meses_nomes}
            atendimentos_por_local[local][mes] += 1

        # Adicionando total por local
        for local, meses_totais in atendimentos_por_local.items():
            meses_totais["Total"] = sum(meses_totais.values())

        # Preenchendo os dados na tabela
        totais_por_mes = {mes: 0 for mes in meses_nomes}  # Inicia os totais por mês
        total_geral = 0

        for local, meses_totais in atendimentos_por_local.items():
            linha = [local]
            for mes in meses_nomes:
                valor = meses_totais.get(mes, 0)
                linha.append(valor)
                totais_por_mes[mes] += valor  # Soma os valores por mês
            total_local = meses_totais["Total"]
            linha.append(total_local)
            total_geral += total_local  # Soma o total geral
            tabela_dados.append(linha)

        # Adiciona a linha de totais no final
        linha_totais = ["Total"]
        for mes in meses_nomes:
            linha_totais.append(totais_por_mes[mes])
        linha_totais.append(total_geral)
        tabela_dados.append(linha_totais)

        # Estilizando a tabela
        tabela = Table(tabela_dados)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Corpo
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Linha de totais
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Cor da linha de totais
        ]))

        # Construindo o documento
        elementos = [elemento_titulo, espaçamento, tabela]
        pdf.build(elementos)
        buffer.seek(0)

        return FileResponse(buffer, filename=f"relatorio_{ano}.pdf")      


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

