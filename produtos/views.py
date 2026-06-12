from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Produto

def index(request):
    produtos = Produto.objects.filter(ativo=True)

    categorias = {}

    for produto in produtos:
        categoria = produto.get_categoria_display()
        
        if categoria not in categorias:
            categorias[categoria] = []
        
        categorias[categoria].append(produto)

    return render(request, 'pages/index.html', {'categorias': categorias})


def produto_detail(request, pk):
    produto = get_object_or_404(Produto, id=pk)
    return render(request, 'pages/produto.html', {'produto': produto})

def produto_detail(request, pk):
    produto = Produto.objects.get(id=pk)
    return render(request, 'pages/produto_detail.html', {
        'produto': produto
    })