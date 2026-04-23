from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'valor', 'data_pagamento')
    list_filter = ('tipo', 'data_pagamento')
    search_fields = ('cliente__nome', 'cliente__sobrenome')
    date_hierarchy = 'data_pagamento'
    ordering = ('-data_pagamento',)