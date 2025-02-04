# atendimento/admin.py

from django.contrib import admin
from .models import LocalServico, Area, Atendimento

admin.site.register(LocalServico)
admin.site.register(Area)
admin.site.register(Atendimento)