from django.db import models
from django.core.exceptions import ValidationError


class TermoSaida(models.Model):
    STATUS_ABERTO = "ABERTO"
    STATUS_DEVOLVIDO = "DEVOLVIDO"

    STATUS_CHOICES = [
        (STATUS_ABERTO, "Aberto"),
        (STATUS_DEVOLVIDO, "Devolvido"),
    ]

    data_retirada = models.DateField("Data de Retirada")
    destino = models.CharField("Destino", max_length=120)

    responsavel = models.CharField("Responsável", max_length=120, default="Não informado")
    produto = models.CharField("Produto", max_length=120, blank=True, default="")
    patrimonio = models.CharField("Patrimônio", max_length=60, blank=True, default="")

    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default=STATUS_ABERTO)
    data_devolucao = models.DateField("Data de Devolução", null=True, blank=True)

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def clean(self):
        if self.status == self.STATUS_DEVOLVIDO and not self.data_devolucao:
            raise ValidationError({"data_devolucao": "Informe a data de devolução quando o status for DEVOLVIDO."})

        if self.status == self.STATUS_ABERTO:
            self.data_devolucao = None

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        base = f"{self.produto or 'Bem'}"
        if self.patrimonio:
            base += f" ({self.patrimonio})"
        return f"{base} - {self.responsavel} [{self.get_status_display()}]"