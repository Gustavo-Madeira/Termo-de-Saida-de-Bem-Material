from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class TermoSaida(models.Model):
    STATUS_ABERTO = "ABERTO"
    STATUS_DEVOLVIDO = "DEVOLVIDO"
    STATUS_CHOICES = [
        (STATUS_ABERTO, "Aberto"),
        (STATUS_DEVOLVIDO, "Devolvido"),
    ]

    data_retirada = models.DateField()
    destino = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    produto = models.CharField(max_length=100)
    patrimonio = models.CharField(max_length=100)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_ABERTO,
    )
    data_devolucao = models.DateField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def clean(self):
        # Normaliza destino em maiúsculo
        if self.destino:
            self.destino = self.destino.upper()

        # Regras de devolução
        if self.status == self.STATUS_ABERTO:
            self.data_devolucao = None

        if self.status == self.STATUS_DEVOLVIDO and not self.data_devolucao:
            raise ValidationError(
                {"data_devolucao": "Informe a data de devolução para status DEVOLVIDO."}
            )

    def save(self, *args, **kwargs):
        """
        Safety-net: garante que atualizado_em nunca vá NULL,
        mesmo se teu banco estiver com esquema “antigo/bugado”.
        """
        if not self.criado_em:
            self.criado_em = timezone.now()
        self.atualizado_em = timezone.now()

        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-data_retirada", "-id"]

    def __str__(self):
        return f"{self.produto} ({self.patrimonio}) - {self.status}"
