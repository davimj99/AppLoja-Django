from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from produtos.models import Produto
from .models import Carrinho, ItemCarrinho

@login_required
def ver_carrinho(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    return render(request, "carrinho.html", {"carrinho": carrinho})


@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)

    item, criado = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto
    )

    if not criado:
        item.quantidade += 1
        item.save()

    return redirect("ver_carrinho")


@login_required
def checkout(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        carrinho.delete()
        return render(request, "checkout_sucesso.html")

    return render(request, "checkout.html", {"carrinho": carrinho})