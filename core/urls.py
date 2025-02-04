# core/urls.py (ou o caminho correto do seu arquivo urls.py)
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importe as views de autenticação
from compaz import views  # Importe suas views personalizadas, se necessário

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Use auth_views.LoginView
    path('signup/', views.signup, name='signup'),  # View de cadastro personalizada
    path('atendimento/', include('compaz.urls')),  # Inclua as URLs da aplicação atendimento
]