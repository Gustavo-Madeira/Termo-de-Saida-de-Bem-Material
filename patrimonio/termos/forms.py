from django import forms
from django.utils import timezone

from .models import TermoSaida


class RegistrarSaidaForm(forms.ModelForm):
    class Meta:
        model = TermoSaida
        fields = ["data_retirada", "destino", "responsavel", "produto", "patrimonio"]

        widgets = {
            "data_retirada": forms.DateInput(attrs={"type": "date"}),
            "destino": forms.TextInput(attrs={"style": "text-transform: uppercase;"}),
        }


class EditarSaidaForm(forms.ModelForm):
    class Meta:
        model = TermoSaida
        fields = ["status", "data_devolucao"]

        widgets = {
            "data_devolucao": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")
        data_dev = cleaned.get("data_devolucao")

        # Se devolvido, data devolução é obrigatória
        if status == TermoSaida.STATUS_DEVOLVIDO and not data_dev:
            self.add_error("data_devolucao", "Informe a data de devolução.")

        # Se aberto, não deixa salvar data devolução
        if status == TermoSaida.STATUS_ABERTO:
            cleaned["data_devolucao"] = None

        return cleaned
