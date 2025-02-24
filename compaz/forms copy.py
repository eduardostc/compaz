from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Atendimento
from compaz.models import CustomUsuario  # Importa o modelo da app usuario
import requests
from datetime import datetime

class AtendimentoForm(forms.ModelForm):
    nome_servico = forms.ChoiceField(choices=[])  # Define o campo como ChoiceField
    forma_atendimento = forms.ChoiceField(
        choices=Atendimento.FORMA_ATENDIMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Atendimento
        fields = [
            'atendente', 'email_atendente', 'data_atendimento', 'turno',
            'local_servico', 'area', 'nome_servico', 'nome_cidadao',
            'telefone_cidadao', 'forma_atendimento', 'problema_resolvido'
        ]
        widgets = {
            'data_atendimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'},
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AtendimentoForm, self).__init__(*args, **kwargs)

        if user:
            self.initial['atendente'] = user.id
            self.fields['atendente'].disabled = True
            self.initial['email_atendente'] = user.email
            self.fields['email_atendente'].disabled = True
            self.initial['data_atendimento'] = datetime.now().date()
            self.fields['data_atendimento'].disabled = True

        # Definir turno automaticamente
        hora_atual = datetime.now().hour
        self.initial['turno'] = 'manha' if 6 <= hora_atual < 12 else 'tarde'
        self.fields['turno'].widget.attrs['disabled'] = 'disabled'

        # Buscar serviços da API
        try:
            response = requests.get('https://carta-servicos-service.app.recife.pe.gov.br/cats/servicos?user_key=54db39aa505b40e86f020769a5d05097&quantidade=9999')
            data = response.json()
            servicos = data.get("resposta", {}).get("dados", [])
            self.fields['nome_servico'].choices = [(servico["nome"], servico["nome"]) for servico in servicos]
        except Exception as e:
            print(f"Erro ao buscar serviços da API: {e}")
            self.fields['nome_servico'].choices = []

class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone', 'email')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')