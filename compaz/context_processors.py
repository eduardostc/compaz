from django.contrib.auth.models import Group

def is_gerente_context(request):
    if request.user.is_authenticated:  # Verifica se o usuário está autenticado
        is_gerente = request.user.groups.filter(name="Gerentes de Atendimento").exists()
    else:
        is_gerente = False  # Usuários não autenticados não são gerentes
    return {'is_gerente': is_gerente}


def is_gestor_context(request):
    if request.user.is_authenticated:  # Verifica se o usuário está autenticado
        is_gestor = request.user.groups.filter(name="Gestores de Relatórios").exists()
    else:
        is_gestor = False  # Usuários não autenticados não são gestores
    return {'is_gestor': is_gestor}

def pertence_grupo_exclusao_context(request):
    if request.user.is_authenticated:  # Verifica se o usuário está autenticado
        pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()
    else:
        pertence_grupo_exclusao = False  # Usuários não autenticados não pertencem ao grupo
    return {'pertence_grupo_exclusao': pertence_grupo_exclusao}