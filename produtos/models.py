from django.db import models

class Produto(models.Model):
    CATEGORIAS = [
        ('apple', 'Apple'),
        ('xbox', 'Xbox'),
        ('playstation', 'Playstation'),
        ('relogio', 'Relógios'),
        ('macbook', 'Macbook'),
        ('fones', 'Fones'),
        ('gamer', 'Gamer'),
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


class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome