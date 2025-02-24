# compaz/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from compaz.models import CustomUsuario, LocalServico, Area, Atendimento
from unittest.mock import patch

class AtendimentoViewsTest(TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.client = Client()
        self.user = CustomUsuario.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            fone='1234567890'
        )
        self.local_servico = LocalServico.objects.create(nome='Local Teste')
        self.area = Area.objects.create(nome='Area Teste')

        # Mock global da API para todos os testes
        self.mock_get_patcher = patch('requests.get')
        self.mock_get = self.mock_get_patcher.start()
        self.mock_get.return_value.json.return_value = {
            "resposta": {
                "dados": [{"nome": "Serviço Teste"}]
            }
        }

    def tearDown(self):
        # Encerra o mock após cada teste
        self.mock_get_patcher.stop()

    def test_criar_atendimento_get(self):
        # Testa a view criar_atendimento com método GET
        self.client.force_login(self.user)  # Autentica o usuário
        response = self.client.get(reverse('criar_atendimento'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # Usar response.context em vez de response.context_data

    def test_criar_atendimento_post(self):
        # Testa a view criar_atendimento com método POST
        self.client.force_login(self.user)  # Autentica o usuário
        data = {
            'atendente': self.user.id,
            'email_atendente': self.user.email,
            'data_atendimento': '2023-10-01',
            'turno': 'manha',
            'local_servico': self.local_servico.id,
            'area': self.area.id,
            'nome_servico': 'Serviço Teste',
            'nome_cidadao': 'Cidadão Teste',
            'telefone_cidadao': '987654321',
            'forma_atendimento': 'notebook',
            'problema_resolvido': True,
        }
        response = self.client.post(reverse('criar_atendimento'), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertEqual(Atendimento.objects.count(), 1)

    def test_lista_atendimentos(self):
        # Testa a view lista_atendimentos
        self.client.force_login(self.user)  # Autentica o usuário
        atendimento = Atendimento.objects.create(
            atendente=self.user,
            email_atendente=self.user.email,
            data_atendimento='2023-10-01',
            turno='manha',
            local_servico=self.local_servico,
            area=self.area,
            nome_servico='Serviço Teste',
            nome_cidadao='Cidadão Teste',
            telefone_cidadao='987654321',
            forma_atendimento='notebook',
            problema_resolvido=True,
        )
        response = self.client.get(reverse('lista_atendimentos'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('atendimentos', response.context)  # Usar response.context em vez de response.context_data
        self.assertEqual(len(response.context['atendimentos']), 1)
        self.assertEqual(response.context['atendimentos'][0], atendimento)