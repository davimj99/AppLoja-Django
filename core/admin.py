from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Produto, Cliente, Pagamento, Pedido, ItemPedido,
    Endereco, EstoqueMovimento, Entrega, Fornecedor,
    Carrinho, ItemCarrinho
)

# -------------------------------
# Cabeçalho do admin
# -------------------------------
admin.site.site_header = "Administração da Loja"
admin.site.site_title = "Administração LOJA"
admin.site.index_title = "Painel Administrativo"

# -------------------------------
# Produto
# -------------------------------
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'categoria', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'estoque', 'ativo')
    ordering = ('nome',)

# -------------------------------
# Cliente
# -------------------------------
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email')
    search_fields = ('nome', 'sobrenome', 'email')
    ordering = ('nome',)

# -------------------------------
# Pagamento
# -------------------------------
@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'valor', 'data_pagamento')
    list_filter = ('tipo', 'data_pagamento')
    search_fields = ('cliente__nome', 'cliente__sobrenome')
    date_hierarchy = 'data_pagamento'

# -------------------------------
# Item do Pedido (Inline)
# -------------------------------
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    fields = ('produto', 'quantidade', 'preco_unitario')
    autocomplete_fields = ('produto',)

# -------------------------------
# Pedido
# -------------------------------
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data', 'status_colored', 'itens_count', 'valor_total')
    list_filter = ('status', 'data')
    search_fields = ('cliente__nome', 'cliente__sobrenome')
    inlines = [ItemPedidoInline]
    date_hierarchy = 'data'
    ordering = ('-data',)

    def valor_total(self, obj):
        return f"R$ {obj.total():.2f}"
    valor_total.short_description = 'Total'

    def itens_count(self, obj):
        return sum(item.quantidade for item in obj.itens.all())
    itens_count.short_description = 'Qtd. Itens'

    def status_colored(self, obj):
        color = {
            'pendente': 'orange',
            'pago': 'green',
            'cancelado': 'red',
        }.get(obj.status, 'black')
        return format_html('<b><span style="color: {};">{}</span></b>', color, obj.status.title())
    status_colored.short_description = 'Status'

# -------------------------------
# Endereço
# -------------------------------
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'cidade', 'estado', 'cep')
    search_fields = ('cliente__nome', 'cidade', 'cep')

# -------------------------------
# Fornecedor
# -------------------------------
@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "telefone", "email")
    search_fields = ("nome", "cnpj")

# -------------------------------
# Estoque
# -------------------------------
@admin.register(EstoqueMovimento)
class EstoqueMovimentoAdmin(admin.ModelAdmin):
    list_display = ("produto", "tipo", "quantidade", "fornecedor", "data")
    list_filter = ("tipo", "data")
    search_fields = ("produto__nome", "fornecedor__nome")

# -------------------------------
# Entrega
# -------------------------------
@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ("pedido", "status_colored", "transportadora", "codigo_rastreio", "data_envio", "data_entrega")
    list_filter = ("status", "transportadora")
    search_fields = ("pedido__id", "codigo_rastreio")

    def status_colored(self, obj):
        color = {
            'pendente': 'orange',
            'enviado': 'blue',
            'entregue': 'green',
            'cancelado': 'red',
        }.get(obj.status, 'black')
        return format_html('<b><span style="color: {};">{}</span></b>', color, obj.status.title())
    status_colored.short_description = 'Status'

# -------------------------------
# Carrinho e ItemCarrinho
# -------------------------------
class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 1
    fields = ('produto', 'quantidade', 'preco_unitario')
    autocomplete_fields = ('produto',)

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status', 'criado_em', 'total_valor')
    list_filter = ('status', 'criado_em')
    search_fields = ('usuario__username',)
    inlines = [ItemCarrinhoInline]
    date_hierarchy = 'criado_em'

    def total_valor(self, obj):
        return f"R$ {obj.total():.2f}"
    total_valor.short_description = 'Total'
