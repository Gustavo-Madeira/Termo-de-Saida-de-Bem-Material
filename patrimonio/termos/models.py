from django.conf import settings
from django.db import models
from django.utils import timezone


class TermoSaida(models.Model):
    """
    Cabeçalho do termo.
    No Excel você tinha tudo por linha, mas no sistema a gente separa:
    - Termo (data, destino, criado_por)
    - Itens do termo (patrimônio, descrição, assinaturas, devolução)
    """

    class Status(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        PARCIAL = "PARCIAL", "Parcial"
        DEVOLVIDO = "DEVOLVIDO", "Devolvido"

    responsavel_nome = models.CharField(max_length=120)
    numero = models.CharField(max_length=20, unique=True, blank=True)  # ex: 2026-000001
    data_retirada = models.DateField(default=timezone.localdate)
    destino = models.CharField(max_length=120)

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ABERTO)

    def __str__(self):
        return self.numero or f"Termo #{self.pk}"

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)

        # Gera número automático depois de ter pk
        if creating and not self.numero:
            ano = timezone.localdate().year
            self.numero = f"{ano}-{self.pk:06d}"
            super().save(update_fields=["numero"])

    def recalcular_status(self):
        itens = self.itens.all()
        if not itens.exists():
            novo = self.Status.ABERTO
        else:
            devolvidos = sum(1 for i in itens if i.data_devolucao)
            if devolvidos == 0:
                novo = self.Status.ABERTO
            elif devolvidos == itens.count():
                novo = self.Status.DEVOLVIDO
            else:
                novo = self.Status.PARCIAL

        if self.status != novo:
            self.status = novo
            self.save(update_fields=["status"])


class ItemTermo(models.Model):
    """
    Cada linha do Excel vira um ItemTermo.
    Colunas do Excel:
    - Data de Retirada -> no TermoSaida
    - Nº do Patrimônio -> aqui
    - Descrição do Bem -> aqui
    - Destino -> no TermoSaida
    - Ass. de Retirada -> aqui
    - Data de Devolução -> aqui
    - Ass. de Devolução -> aqui
    """

    termo = models.ForeignKey(TermoSaida, related_name="itens", on_delete=models.CASCADE)

    patrimonio_num = models.CharField(max_length=50)
    descricao_bem = models.CharField(max_length=255)

    assinatura_retirada = models.CharField(max_length=120, blank=True)
    data_devolucao = models.DateField(null=True, blank=True)
    assinatura_devolucao = models.CharField(max_length=120, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patrimonio_num} - {self.descricao_bem}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # sempre que item muda, recalcula status do termo
        if self.termo_id:
            self.termo.recalcular_status()
