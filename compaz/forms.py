# atendimento/forms.py
from django import forms
from .models import Atendimento
import requests
from datetime import datetime
# atendimento/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['local_servico', 'area', 'nome_servico', 'nome_cidadao', 'telefone_cidadao', 'forma_atendimento', 'problema_resolvido']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AtendimentoForm, self).__init__(*args, **kwargs)
        
        if user:
            # Define o valor inicial do campo 'atendente' (que é um ForeignKey para o modelo User)
            self.initial['atendente'] = user.id
            # Define o valor inicial do campo 'email_atendente'
            self.initial['email_atendente'] = user.email

        # Preencher o turno automaticamente
        hora_atual = datetime.now().hour
        if 6 <= hora_atual < 12:
            self.initial['turno'] = 'manha'
        elif 12 <= hora_atual < 18:
            self.initial['turno'] = 'tarde'

        # Buscar serviços da API
        response = requests.get('https://carta-servicos-service.app.recife.pe.gov.br/cats/servicos?user_key=54db39aa505b40e86f020769a5d05097&quantidade=9999')
        data = response.json()
        servicos = data.get("resposta", {}).get("dados", [])  # Acessa a chave correta no JSON
        self.fields['nome_servico'].choices = [(servico["nome"], servico["nome"]) for servico in servicos]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Informe um email válido.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')