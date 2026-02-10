from django.db import models
from django.utils import timezone


class TermoSaida(models.Model):
    STATUS_ABERTO = "ABERTO"
    STATUS_DEVOLVIDO = "DEVOLVIDO"

    STATUS_CHOICES = (
        (STATUS_ABERTO, "ABERTO"),
        (STATUS_DEVOLVIDO, "DEVOLVIDO"),
    )

    data_retirada = models.DateField()
    destino = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=200)
    produto = models.CharField(max_length=200)
    patrimonio = models.CharField(max_length=100)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ABERTO)
    data_devolucao = models.DateField(null=True, blank=True)

    criado_em = models.DateTimeField(default=timezone.now, editable=False)
    atualizado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-data_retirada", "-id"]  # ✅ mais novo primeiro

    def save(self, *args, **kwargs):
        self.atualizado_em = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto} ({self.patrimonio}) - {self.responsavel}"
