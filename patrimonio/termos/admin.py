from django.contrib import admin
from .models import TermoSaida


@admin.register(TermoSaida)
class TermoSaidaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "data_retirada",
        "destino",
        "responsavel",
        "produto",
        "patrimonio",
        "status",
        "data_devolucao",
        "criado_em",
    )
    list_filter = ("status", "data_retirada", "destino")
    search_fields = ("destino", "responsavel", "produto", "patrimonio")
    ordering = ("-criado_em",)