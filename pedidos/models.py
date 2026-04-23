from django.db import models
from clientes.models import Cliente
from produtos.models import Produto
from pagamentos.models import Pagamento


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    pagamento = models.OneToOneField(Pagamento, on_delete=models.SET_NULL, null=True, blank=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario


class Entrega(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='entrega')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    transportadora = models.CharField(max_length=100, blank=True, null=True)
    codigo_rastreio = models.CharField(max_length=50, blank=True, null=True)