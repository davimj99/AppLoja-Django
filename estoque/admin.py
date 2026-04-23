from django.contrib import admin
from .models import EstoqueMovimento


@admin.register(EstoqueMovimento)
class EstoqueMovimentoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'fornecedor', 'data')
    list_filter = ('tipo', 'data', 'fornecedor')
    search_fields = ('produto__nome', 'fornecedor__nome')
    date_hierarchy = 'data'