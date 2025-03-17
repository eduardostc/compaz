from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Atendimento, LocalServico, Area
from compaz.models import CustomUsuario  # Importa o modelo da app usuario
import requests
from datetime import datetime

# forms.py

class AtendimentoForm(forms.ModelForm):
    # nome_servico = forms.ChoiceField(choices=[])  # Define o campo como ChoiceField
    nome_servico = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),  # Garante que o select tenha a classe correta
    )
    forma_atendimento = forms.ChoiceField(
        choices=Atendimento.FORMA_ATENDIMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    local_servico = forms.ModelChoiceField(
        queryset=LocalServico.objects.all(),
        required=False,  # Defina como True se o campo for obrigatório
        label="Local do Serviço"
    )
    area = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        required=False,  # Defina como True se o campo for obrigatório
        label="Área"
    )

    class Meta:
        model = Atendimento
        fields = [
            'atendente', 'email_atendente', 'data_atendimento', 'turno',
            'local_servico', 'area', 'nome_servico', 'nome_cidadao',
            'telefone_cidadao', 'forma_atendimento', 'problema_resolvido',
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

        #Isso garante que todos os campos do formulário herdem a classe de estilo básico para o Bootstrap.
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:  # Adiciona a classe apenas se ela não existir
                field.widget.attrs['class'] = 'form-control'
        
        # Adiciona classe específica ao checkbox do campo "problema_resolvido"
        if 'problema_resolvido' in self.fields:
            self.fields['problema_resolvido'].widget.attrs.update({'class': 'form-check-input'})


        if user:
            self.initial['atendente'] = user
            self.fields['atendente'].queryset = CustomUsuario.objects.filter(id=user.id)
            self.fields['atendente'].disabled = True
            
            self.initial['email_atendente'] = user.email
            self.fields['email_atendente'].disabled = True

            self.initial['data_atendimento'] = datetime.now().date()
            self.fields['data_atendimento'].disabled = True
            # self.fields['data_atendimento'].widget.attrs['readonly'] = True  # Tornar o campo somente leitura

            # Define o valor inicial do campo local_servico com base no usuário logado
            if user.local_servico:
                self.initial['local_servico'] = user.local_servico
                self.fields['local_servico'].disabled = True

            # Define o valor inicial do campo area com base no usuário logado
            if user.area:
                self.initial['area'] = user.area
                self.fields['area'].disabled = True

        # Definir turno automaticamente
        hora_atual = datetime.now().hour
        self.initial['turno'] = 'manha' if 6 <= hora_atual < 12 else 'tarde'
        # self.fields['turno'].widget.attrs['disabled'] = 'disabled'
        # self.fields['turno'].widget.attrs['readonly'] = True  # Tornar o campo somente leitura
        self.fields['turno'].widget = forms.HiddenInput()  # Usar um campo oculto para o turno

        # Adiciona uma opção padrão ao campo nome_servico
        self.fields['nome_servico'].choices = [('', 'Selecione um serviço')]

        # Buscar serviços da API
        try:
            response = requests.get('https://carta-servicos-service.app.recife.pe.gov.br/cats/servicos?user_key=54db39aa505b40e86f020769a5d05097&quantidade=9999')
            data = response.json()
            servicos = data.get("resposta", {}).get("dados", [])
            # Adiciona os serviços da API às escolhas existentes
            self.fields['nome_servico'].choices += [(servico["nome"], servico["nome"]) for servico in servicos]
        except Exception as e:
            print(f"Erro ao buscar serviços da API: {e}")
            # Mantém a opção padrão em caso de erro
            self.fields['nome_servico'].choices = [('', 'Selecione um serviço')]
            if not self.fields['nome_servico'].choices or len(self.fields['nome_servico'].choices) == 1:
                self.fields['nome_servico'].choices += [('default', 'Serviço Default')]
            
            

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
