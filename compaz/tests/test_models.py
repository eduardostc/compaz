import uuid
from django.test import TestCase
from model_bakery import baker  # model_mommy foi descontinuado

from compaz.models import CustomUsuario, LocalServico, Area, Atendimento


from django.test import TestCase
from compaz.models import CustomUsuario


class UsuarioManagerTestCase(TestCase):

    def test_create_user(self):
        """Testa a criação de um usuário comum"""
        user = CustomUsuario.objects.create_user(email="user@exemplo.com", password="testpassword")

        self.assertIsInstance(user, CustomUsuario)
        self.assertEqual(user.email, "user@exemplo.com")
        self.assertFalse(user.is_superuser)  # Deve ser False para usuários normais
        self.assertFalse(user.is_staff)  # Deve ser False por padrão

    def test_create_user_without_email(self):
        """Testa a criação de um usuário sem e-mail (deve gerar erro)"""
        with self.assertRaises(ValueError) as context:
            CustomUsuario.objects.create_user(email="", password="testpassword")
        
        self.assertEqual(str(context.exception), "O e-mail é obrigatório")

    def test_create_superuser(self):
        """Testa a criação de um superusuário"""
        superuser = CustomUsuario.objects.create_superuser(email="admin@exemplo.com", password="adminpassword")

        self.assertIsInstance(superuser, CustomUsuario)
        self.assertEqual(superuser.email, "admin@exemplo.com")
        self.assertTrue(superuser.is_superuser)  # Deve ser True
        self.assertTrue(superuser.is_staff)  # Deve ser True

    def test_create_superuser_without_is_superuser(self):
        """Testa se criar um superusuário sem is_superuser=True gera erro"""
        with self.assertRaises(ValueError) as context:
            CustomUsuario.objects.create_superuser(email="admin@exemplo.com", password="adminpassword", is_superuser=False)

        self.assertEqual(str(context.exception), "Superuser precisa ter is_superuser=True")

    def test_create_superuser_without_is_staff(self):
        """Testa se criar um superusuário sem is_staff=True gera erro"""
        with self.assertRaises(ValueError) as context:
            CustomUsuario.objects.create_superuser(email="admin@exemplo.com", password="adminpassword", is_staff=False)

        self.assertEqual(str(context.exception), "Superuser precisa ter is_staff=True")


#------------------------------------------------------------------------------------------------
class ModelsTestCase(TestCase):

    def setUp(self):
        # Criar instâncias para os testes
        self.usuario = baker.make(CustomUsuario, email="teste@exemplo.com")
        self.local_servico = baker.make(LocalServico, nome="Unidade Central")
        self.area = baker.make(Area, nome="Saúde")
        self.atendimento = baker.make(Atendimento, nome_cidadao="João Silva")

    def test_custom_usuario_str(self):
        """Testa o método __str__ do modelo CustomUsuario"""
        #self.assertEqual(str(self.usuario), self.usuario.email)
        self.assertEqual(str(self.usuario), f"{self.usuario.first_name} {self.usuario.last_name}".strip())

    def test_local_servico_str(self):
        """Testa o método __str__ do modelo LocalServico"""
        self.assertEqual(str(self.local_servico), self.local_servico.nome)

    def test_area_str(self):
        """Testa o método __str__ do modelo Area"""
        self.assertEqual(str(self.area), self.area.nome)

    def test_atendimento_str(self):
        """Testa o método __str__ do modelo Atendimento"""
        expected_str = f"Atendimento {self.atendimento.id} - {self.atendimento.nome_cidadao}"
        self.assertEqual(str(self.atendimento), expected_str)










# import uuid
# from django.test import testcases
# from model_mommy import mommy

# from compaz.models import get_file_path

# class ServicoTestCase(TestCase):
    
#     def setUp(self):
#         self.servico = mommy.make('Servico')

#     def test_str(self):
#         self.assertEquals(str(self.servico), self.servico.servico)