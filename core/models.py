from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# Produto
# -------------------------------
class Produto(models.Model):   
    CATEGORIAS = [
        ('apple', 'Apple'),
        ('xbox', 'Xbox'),
        ('playstation', 'Playstation'),
        ('relogio', 'Relógios'),
        ('macbook', 'Macbook'),
        ('fones', 'Fones'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True, null=True)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=10)
    estoque = models.PositiveIntegerField('Quantidade em Estoque', default=0)
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
class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class TipoPagamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Pagamento(models.Model):
    TIPOS = [
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    ]

    nome = models.CharField('Nome do Pagador', max_length=100)
    tipo = models.CharField('Tipo de Pagamento', max_length=20, choices=TIPOS)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField('Data do Pagamento', auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.tipo} - R${self.valor}'


# -------------------------------
# Pedido
# -------------------------------
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ], default='pendente')
    pagamento = models.OneToOneField(Pagamento, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome}'

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())


# -------------------------------
# Item do Pedido
# -------------------------------
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField('Quantidade', default=1)
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})'

    def subtotal(self):
        return self.quantidade * self.preco_unitario

# -------------------------------
# Carrinho e ItemCarrinho
# -------------------------------
class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name="itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="enderecos")
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # UF
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

# -------------------------------
# Movimentação de Estoque
# -------------------------------
class EstoqueMovimento(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("saida", "Saída"),
    ]

    produto = models.ForeignKey("Produto", on_delete=models.CASCADE, related_name="movimentos")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo} ({self.quantidade})"

# -------------------------------
# Entrega do Pedido
# -------------------------------
class Entrega(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("enviado", "Enviado"),
        ("entregue", "Entregue"),
        ("cancelado", "Cancelado"),
    ]

    pedido = models.OneToOneField("Pedido", on_delete=models.CASCADE, related_name="entrega")
    transportadora = models.CharField(max_length=100, blank=True, null=True)
    codigo_rastreio = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    data_envio = models.DateTimeField(blank=True, null=True)
    data_entrega = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Entrega #{self.pedido.id} - {self.status}"