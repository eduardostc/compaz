from unittest.mock import patch
from django.test import TestCase
from compaz.forms import AtendimentoForm, CustomUsuarioCreateForm, CustomUsuarioChangeForm
from compaz.models import CustomUsuario, LocalServico, Area
from datetime import datetime


class AtendimentoFormTest(TestCase):

    def setUp(self):
        """Cria um usuário de teste para ser usado nos formulários."""
        self.user = CustomUsuario.objects.create_user(
            email="teste@exemplo.com",
            password="senha123",
            first_name="Teste",
            last_name="Usuário"
        )
        self.local_servico = LocalServico.objects.create(nome="Unidade Central")
        self.area = Area.objects.create(nome="Saúde")

    def test_form_init_with_user(self):
        """Testa se os campos do formulário são inicializados corretamente com um usuário."""
        form = AtendimentoForm(user=self.user)

        self.assertEqual(str(form.initial['atendente']), self.user.get_full_name())
        self.assertTrue(form.fields['atendente'].disabled)

        self.assertEqual(form.initial['email_atendente'], self.user.email)
        self.assertTrue(form.fields['email_atendente'].disabled)

    def test_form_turno_auto_set(self):
        """Testa se o turno é definido corretamente com base no horário."""
        form = AtendimentoForm()
        turno_esperado = 'manha' if 6 <= datetime.now().hour < 12 else 'tarde'
        self.assertEqual(form.initial['turno'], turno_esperado)

    def test_form_api_servicos(self):
        """Testa se os serviços são carregados da API corretamente."""
        form = AtendimentoForm()
        self.assertIsInstance(form.fields['nome_servico'].choices, list)

    def test_api_servicos_falha(self):
        """Testa se o formulário lida corretamente com erro na API."""
        with patch('requests.get') as mock_get:
            # Simula um erro na API
            mock_get.side_effect = Exception("Erro simulado na API")

            # Cria o formulário
            form = AtendimentoForm(user=self.user)

            # Verifica se as escolhas do campo nome_servico estão corretas
            self.assertEqual(form.fields['nome_servico'].choices, [('', 'Selecione um serviço')])

    def test_form_clean(self):
        """Testa a lógica de validação do formulário."""
        form_data = {
            'atendente': self.user,
            'email_atendente': self.user.email,
            'data_atendimento': datetime.now().date(),
            'turno': 'manha',
            'local_servico': None,  # Simula um erro de validação
            'area': None,  # Simula um erro de validação
            'nome_servico': 'Serviço Teste',
            'nome_cidadao': 'Cidadão Teste',
            'telefone_cidadao': '987654321',
            'forma_atendimento': 'notebook',
            'problema_resolvido': True,
        }
        form = AtendimentoForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('local_servico', form.errors)
        self.assertIn('area', form.errors)


class CustomUsuarioCreateFormTest(TestCase):

    def test_usuario_create_form_save(self):
        """Testa se o formulário de criação de usuário salva corretamente."""
        form_data = {
            "first_name": "Teste",
            "last_name": "Usuário",
            "fone": "81999999999",
            "email": "teste@exemplo.com",
            "password1": "senha1234",
            "password2": "senha1234",
        }

        form = CustomUsuarioCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

        usuario = form.save()
        
        # Verifica se os dados foram salvos corretamente
        self.assertEqual(usuario.email, "teste@exemplo.com")
        self.assertEqual(usuario.username, "teste@exemplo.com")
        self.assertTrue(usuario.check_password("senha1234"))

    def test_usuario_create_form_clean(self):
        """Testa a lógica de validação do formulário de criação de usuário."""
        form_data = {
            'first_name': 'Teste',
            'last_name': 'Usuário',
            'fone': '81999999999',
            'email': 'teste@exemplo.com',
            'password1': 'senha1234',
            'password2': 'senha1234',
        }
        form = CustomUsuarioCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class CustomUsuarioChangeFormTest(TestCase):

    def test_usuario_change_form_init(self):
        """Testa a inicialização do formulário de edição de usuário."""
        form = CustomUsuarioChangeForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('fone', form.fields)