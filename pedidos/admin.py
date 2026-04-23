from django.contrib import admin
from .models import Pedido, ItemPedido, Entrega
from django.utils.html import format_html


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data', 'status', 'total')
    list_filter = ('status', 'data')
    search_fields = ('cliente__nome',)
    inlines = [ItemPedidoInline]
    date_hierarchy = 'data'

    def total(self, obj):
        return f"R$ {obj.total():.2f}"


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'status', 'transportadora', 'codigo_rastreio')
    list_filter = ('status',)


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'preco_unitario')