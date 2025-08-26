from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Produto

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
