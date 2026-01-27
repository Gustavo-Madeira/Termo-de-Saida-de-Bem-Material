from django.contrib import admin
from .models import TermoSaida, ItemTermo


class ItemTermoInline(admin.TabularInline):
    model = ItemTermo
    extra = 1


@admin.register(TermoSaida)
class TermoSaidaAdmin(admin.ModelAdmin):
    inlines = [ItemTermoInline]
    list_display = ("numero", "data_retirada", "destino", "status", "criado_por", "criado_em")
    search_fields = ("numero", "destino", "itens__patrimonio_num", "itens__descricao_bem")
    list_filter = ("status", "data_retirada")
    ordering = ("-criado_em",)


@admin.register(ItemTermo)
class ItemTermoAdmin(admin.ModelAdmin):
    list_display = ("termo", "patrimonio_num", "descricao_bem", "data_devolucao")
    search_fields = ("patrimonio_num", "descricao_bem", "termo__numero")
    list_filter = ("data_devolucao",)