from django.contrib import admin
from .models import Carrinho, ItemCarrinho


class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 1


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status', 'criado_em')
    list_filter = ('status',)
    search_fields = ('usuario__username',)
    inlines = [ItemCarrinhoInline]
    date_hierarchy = 'criado_em'