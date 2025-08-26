from django.contrib import admin

# Registrar modelos na administração 
from.models import Produto, Cliente, Pagamento, Pedido 
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email')

class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'valor', 'data_pagamento')

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente','data','status')

admin.site.register(Produto , ProdutoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Pedido, PedidoAdmin)
