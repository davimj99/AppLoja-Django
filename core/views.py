from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from produtos.models import Produto

def home(request):
    produtos = Produto.objects.filter(ativo=True)

    categorias = {}

    for produto in produtos:
        categoria = produto.get_categoria_display()

        if categoria not in categorias:
            categorias[categoria] = []

        categorias[categoria].append(produto)

    return render(request, 'index.html', {'categorias': categorias})

def error404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponse(template.render({}, request), status=404)


def error500(request):
    template = loader.get_template('500.html')
    return HttpResponse(template.render({}, request), status=500)

def contato(request):
    return render(request, 'contato.html')