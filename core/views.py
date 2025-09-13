from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Produto, Carrinho, ItemCarrinho
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Página inicial
def index(request):
    produtos = Produto.objects.all()
    
    # Agrupar produtos por categoria
    categorias = defaultdict(list)
    for produto in produtos:
        categorias[produto.categoria].append(produto)
    
    context = {
        'curso': 'Programação Web com Django Framework',
        'outro': 'Django é massa',
        'categorias': dict(categorias),  # converte defaultdict para dict
    }
    
    return render(request, 'index.html', context)

# Página de contato
def contato(request):
    return render(request, 'contato.html')

# Detalhe do produto
def produto(request, pk):
    prod = get_object_or_404(Produto, id=pk)
    context = {'produto': prod}
    return render(request, 'produto.html', context)

# Página de erro 404
def error404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=404)

# Página de erro 500
def error500(request):
    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=500)

def carrinho_view(request):
    return render(request, 'carrinho.html')
def produtos_view(request):
    # aqui você pode enviar os produtos do banco, se quiser
    return render(request, 'produtos.html')

@login_required
def ver_carrinho(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    return render(request, "carrinho.html", {"carrinho": carrinho})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    item, criado = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    if not criado:
        item.quantidade += 1
        item.save()
    return redirect("ver_carrinho")

@login_required
def checkout(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        # Aqui você pode processar pagamento, salvar pedido etc.
        carrinho.delete()
        return render(request, "checkout_sucesso.html")
    return render(request, "checkout.html", {"carrinho": carrinho})

@staff_member_required
def admin_dashboard(request):
    # Cards principais
    produtos_count = Produto.objects.count()
    categorias_count = Categoria.objects.count()
    pedidos_count = Pedido.objects.count()
    clientes_count = User.objects.count()

    # Alertas: produtos com estoque baixo
    produtos_estoque_baixo = Produto.objects.filter(estoque__lte=5)

    # Gráfico de vendas por categoria
    categorias_labels = []
    categorias_valores = []
    for cat in Categoria.objects.all():
        count = Produto.objects.filter(categoria=cat).count()
        categorias_labels.append(cat.nome)
        categorias_valores.append(count)

    # Gráfico de pedidos por mês (exemplo)
    pedidos_meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    pedidos_meses_valores = [Pedido.objects.filter(data__month=i+1).count() for i in range(6)]

    context = {
        'produtos_count': produtos_count,
        'categorias_count': categorias_count,
        'pedidos_count': pedidos_count,
        'clientes_count': clientes_count,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'categorias_labels': categorias_labels,
        'categorias_valores': categorias_valores,
        'pedidos_meses_labels': pedidos_meses_labels,
        'pedidos_meses_valores': pedidos_meses_valores,
    }
    return render(request, 'admin/base_site.html', context)