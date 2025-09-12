from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Produto, Carrinho, ItemCarrinho
from django.contrib.auth.decorators import login_required

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