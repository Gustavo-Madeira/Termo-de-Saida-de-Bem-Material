from django import forms
from .models import TermoSaida

class RegistrarSaidaForm(forms.ModelForm):
    patrimonio_num = forms.CharField(label="Nº do Patrimônio", max_length=50)
    descricao_bem = forms.CharField(label="Descrição do Bem", max_length=255)

    class Meta:
        model = TermoSaida
        fields = ["data_retirada", "destino", "responsavel_nome"]
        widgets = {"data_retirada": forms.DateInput(attrs={"type": "date"})}
