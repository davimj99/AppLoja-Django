from django.db import models

# -------------------------------
# Produto
# -------------------------------
class Produto(models.Model):   
    CATEGORIAS = [
        ('apple', 'Apple'),
        ('xbox', 'Xbox'),
        ('playstation', 'Playstation'),
        ('relogio', 'Relogios'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=8)
    estoque = models.IntegerField('Quantidade em Estoque')
    imagem = models.ImageField('Imagem do Produto', upload_to='produtos/', null=True, blank=True)
    categoria = models.CharField('Categoria', max_length=20, choices=CATEGORIAS, default='outros')

    def __str__(self):
        return self.nome


# -------------------------------
# Cliente
# -------------------------------
class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sobrenome = models.CharField('Sobrenome', max_length=100)
    email = models.EmailField('E-mail', max_length=100, unique=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


# -------------------------------
# Pagamento
# -------------------------------
class Pagamento(models.Model):
    TIPO_PAGAMENTO = [
        ('crédito', 'Crédito'),
        ('débito', 'Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    ]

    nome = models.CharField('Nome do Pagador', max_length=100)
    tipo = models.CharField('Tipo de Pagamento', max_length=20, choices=TIPO_PAGAMENTO)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField('Data do Pagamento', auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.tipo} - R${self.valor}'


# -------------------------------
# Pedido
# -------------------------------
class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ], default='pendente')
    pagamento = models.OneToOneField('Pagamento', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome}'

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())


# -------------------------------
# Item do Pedido
# -------------------------------
class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField('Quantidade', default=1)
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})'

    def subtotal(self):
        return self.quantidade * self.preco_unitario
