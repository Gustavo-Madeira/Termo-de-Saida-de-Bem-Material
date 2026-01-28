from django.contrib import admin
from .models import TermoSaida


@admin.register(TermoSaida)
class TermoSaidaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "data_retirada",
        "destino",
        "responsavel_nome",
        "produto",
        "patrimonio",
        "status",
        "data_devolucao",
        "criado_em",
    )
    list_filter = ("status", "data_retirada", "data_devolucao", "destino")
    search_fields = ("destino", "responsavel_nome", "produto", "patrimonio")
    ordering = ("-criado_em",)