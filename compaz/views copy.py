# compaz/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AtendimentoForm
from .models import Atendimento
from django.contrib.auth import login


@login_required
def criar_atendimento(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, user=request.user)  # Passa o usuário logado
        if form.is_valid():
            form.save()
            return redirect('lista_atendimentos')
    else:
        form = AtendimentoForm(user=request.user)  # Passa o usuário logado
    return render(request, 'compaz/criar_atendimento.html', {'form': form})


@login_required
def lista_atendimentos(request):
    atendimentos = Atendimento.objects.filter(atendente=request.user) #cada atendente só pode ver seus próprios atendimentos
    #atendimentos = Atendimento.objects.all() #odos os usuários podem ver todos os atendimentos
    return render(request, 'compaz/lista_atendimentos.html', {'atendimentos': atendimentos})




# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Loga o usuário após o cadastro
#             return redirect('criar_atendimento')  # Redireciona para a página de criação de atendimento
#     else:
#         form = SignUpForm()  # Usa o formulário personalizado
#     return render(request, 'registration/signup.html', {'form': form})


# from django.shortcuts import redirect
# from django.contrib.auth import login as auth_login

# def login(request):
#     if request.method == 'POST':
#         # Lógica de autenticação
#         user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             auth_login(request, user)
#             return redirect('pagina_personalizada')  # Redireciona para uma página personalizada
#     return render(request, 'registration/login.html')