from django.db import models
from clientes.models import Cliente


class Pagamento(models.Model):
    TIPOS = [
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.tipo}"