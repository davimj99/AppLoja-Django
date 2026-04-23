from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from produtos.models import Produto
from .models import Pedido

@staff_member_required
def admin_dashboard(request):
    produtos_count = Produto.objects.count()
    pedidos_count = Pedido.objects.count()
    clientes_count = User.objects.count()

    produtos_estoque_baixo = Produto.objects.filter(estoque__lte=5)

    context = {
        "produtos_count": produtos_count,
        "pedidos_count": pedidos_count,
        "clientes_count": clientes_count,
        "produtos_estoque_baixo": produtos_estoque_baixo,
    }

    return render(request, "admin/dashboard.html", context)