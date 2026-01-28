from django.db import models


class TermoSaida(models.Model):
    STATUS_ABERTO = "ABERTO"
    STATUS_DEVOLVIDO = "DEVOLVIDO"

    STATUS_CHOICES = [
        (STATUS_ABERTO, "ABERTO"),
        (STATUS_DEVOLVIDO, "DEVOLVIDO"),
    ]

    data_retirada = models.DateField("Data de Retirada")
    destino = models.CharField("Destino", max_length=120)
    responsavel_nome = models.CharField("Responsável", max_length=120, default="Não informado")

    # >>> ESTES 2 CAMPOS RESOLVEM O PROBLEMA DO PRODUTO/PATRIMÔNIO NA LISTA
    produto = models.CharField("Produto", max_length=120, default="", blank=True)
    patrimonio = models.CharField("Patrimônio", max_length=60, default="", blank=True)

    status = models.CharField("Status", max_length=12, choices=STATUS_CHOICES, default=STATUS_ABERTO)
    data_devolucao = models.DateField("Data de Devolução", null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.destino} - {self.responsavel_nome} ({self.data_retirada})"