from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


UF_CHOICES = [
    ('DF','Distrito Federal'),
    ('SP','São Paulo'),
    # pode completar depois
]

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="enderecos")
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=UF_CHOICES)

    def __str__(self):
        return f"{self.rua}, {self.numero}"