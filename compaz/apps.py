from django.apps import AppConfig
from django.db.utils import OperationalError
from django.contrib.auth import get_user_model

class CompazConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compaz'

    def ready(self):
        User = get_user_model()
        
        try:
            # Verifica se o superusuário já existe
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='carlos.rodrigues@recife.pe.gov.br',
                    password='@Admin123'
                )
                print("Superusuário criado com sucesso!")
        except OperationalError:
            # Isso previne erros durante a migração inicial, quando o banco ainda não está configurado
            pass

