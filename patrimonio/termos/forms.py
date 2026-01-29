from django import forms
from .models import TermoSaida


class RegistrarSaidaForm(forms.ModelForm):
    class Meta:
        model = TermoSaida
        fields = ["data_retirada", "destino", "responsavel", "produto", "patrimonio"]

        widgets = {
            "data_retirada": forms.DateInput(attrs={"type": "date"}),
        }

        labels = {
            "data_retirada": "Data de Retirada",
            "destino": "Destino",
            "responsavel": "Responsável",
            "produto": "Produto",
            "patrimonio": "Patrimônio",
        }


class TermoEditForm(forms.ModelForm):
    class Meta:
        model = TermoSaida
        fields = ["data_retirada", "destino", "responsavel", "produto", "patrimonio", "status", "data_devolucao"]

        widgets = {
            "data_retirada": forms.DateInput(attrs={"type": "date"}),
            "data_devolucao": forms.DateInput(attrs={"type": "date"}),
        }

        labels = {
            "data_retirada": "Data da retirada",
            "destino": "Destino",
            "responsavel": "Responsável",
            "produto": "Produto",
            "patrimonio": "Patrimônio",
            "status": "Status",
            "data_devolucao": "Data de devolução",
        }

        help_texts = {
            "data_devolucao": "Habilita automaticamente quando Status = DEVOLVIDO.",
        }

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")
        data_dev = cleaned.get("data_devolucao")

        if status == TermoSaida.STATUS_DEVOLVIDO and not data_dev:
            self.add_error("data_devolucao", "Informe a data de devolução quando o status for DEVOLVIDO.")

        if status == TermoSaida.STATUS_ABERTO:
            cleaned["data_devolucao"] = None

        return cleaned