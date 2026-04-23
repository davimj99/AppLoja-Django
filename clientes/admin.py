from django.contrib import admin
from .models import Cliente, Endereco


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email')
    search_fields = ('nome', 'sobrenome', 'email')
    ordering = ('nome',)


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'rua', 'numero', 'cidade', 'estado')
    list_filter = ('estado', 'cidade')
    search_fields = ('cliente__nome', 'rua', 'cidade')