from django import forms
from .models import TermoSaida


class RegistrarSaidaForm(forms.ModelForm):
    class Meta:
        model = TermoSaida
        fields = [
            "data_retirada",
            "destino",
            "responsavel_nome",
            "produto",
            "patrimonio",
            "data_devolucao",
        ]
        widgets = {
            "data_retirada": forms.DateInput(attrs={"type": "date"}),
            "data_devolucao": forms.DateInput(attrs={"type": "date"}),
        }


class EditarSaidaForm(forms.ModelForm):
    class Meta:
        model = TermoSaida
        fields = [
            "data_retirada",
            "destino",
            "responsavel_nome",
            "produto",
            "patrimonio",
            "status",
            "data_devolucao",
        ]
        widgets = {
            "data_retirada": forms.DateInput(attrs={"type": "date"}),
            "data_devolucao": forms.DateInput(attrs={"type": "date"}),
        }