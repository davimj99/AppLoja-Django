from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

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

    nome = models.CharField(max_length=100, db_index=True)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='outros')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

# -------------------------------
# Cliente
# -------------------------------
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

# -------------------------------
# Endereço
# -------------------------------
UF_CHOICES = [
    ('AC','Acre'), ('AL','Alagoas'), ('AP','Amapá'), ('AM','Amazonas'),
    ('BA','Bahia'), ('CE','Ceará'), ('DF','Distrito Federal'), ('ES','Espírito Santo'),
    ('GO','Goiás'), ('MA','Maranhão'), ('MT','Mato Grosso'), ('MS','Mato Grosso do Sul'),
    ('MG','Minas Gerais'), ('PA','Pará'), ('PB','Paraíba'), ('PR','Paraná'), 
    ('PE','Pernambuco'), ('PI','Piauí'), ('RJ','Rio de Janeiro'), ('RN','Rio Grande do Norte'),
    ('RS','Rio Grande do Sul'), ('RO','Rondônia'), ('RR','Roraima'), ('SC','Santa Catarina'),
    ('SP','São Paulo'), ('SE','Sergipe'), ('TO','Tocantins'),
]

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="enderecos")
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=UF_CHOICES)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

# -------------------------------
# Fornecedor
# -------------------------------
class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

# -------------------------------
# Pagamento
# -------------------------------
class Pagamento(models.Model):
    TIPOS = [
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pagamentos")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente.nome} - {self.tipo} - R${self.valor}'

# -------------------------------
# Pedido
# -------------------------------
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    pagamento = models.OneToOneField(Pagamento, on_delete=models.SET_NULL, null=True, blank=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome} - {self.status}'

# -------------------------------
# Item do Pedido
# -------------------------------
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})'

# -------------------------------
# Carrinho e ItemCarrinho
# -------------------------------
class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('aberto','Aberto'),('finalizado','Finalizado')], default='aberto')

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name="itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

# -------------------------------
# Movimentação de Estoque
# -------------------------------
class EstoqueMovimento(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("saida", "Saída"),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="movimentos")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.tipo == 'entrada':
            self.produto.estoque += self.quantidade
        elif self.tipo == 'saida':
            self.produto.estoque -= self.quantidade
            if self.produto.estoque < 0:
                self.produto.estoque = 0
        self.produto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo} ({self.quantidade})"

# -------------------------------
# Entrega
# -------------------------------
class Entrega(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("enviado", "Enviado"),
        ("entregue", "Entregue"),
        ("cancelado", "Cancelado"),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="entrega")
    transportadora = models.CharField(max_length=100, blank=True, null=True)
    codigo_rastreio = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    data_envio = models.DateTimeField(blank=True, null=True)
    data_entrega = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Entrega #{self.pedido.id} - {self.status}"
