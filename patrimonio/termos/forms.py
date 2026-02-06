from django import forms
from .models import TermoSaida

DATE_INPUT_FORMATS = ["%Y-%m-%d", "%d/%m/%Y"]


class RegistrarSaidaForm(forms.ModelForm):
    data_retirada = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = TermoSaida
        fields = ["data_retirada", "destino", "responsavel", "produto", "patrimonio"]
        widgets = {
            "destino": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    "autocomplete": "off",
                }
            ),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "produto": forms.TextInput(attrs={"class": "form-control"}),
            "patrimonio": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_destino(self):
        destino = (self.cleaned_data.get("destino") or "").strip()
        return destino.upper()


class EditarSaidaForm(forms.ModelForm):
    data_retirada = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    data_devolucao = forms.DateField(
        required=False,
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = TermoSaida
        fields = [
            "data_retirada",
            "destino",
            "responsavel",
            "produto",
            "patrimonio",
            "status",
            "data_devolucao",
        ]
        widgets = {
            "destino": forms.TextInput(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "produto": forms.TextInput(attrs={"class": "form-control"}),
            "patrimonio": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bloqueia tudo, menos STATUS (e data_devolucao dependendo do status)
        bloqueados = ["data_retirada", "destino", "responsavel", "produto", "patrimonio"]
        for nome in bloqueados:
            self.fields[nome].disabled = True
            self.fields[nome].widget.attrs["class"] = "form-control bloqueado"

        # Decide se data_devolucao deve estar habilitada baseado no STATUS do POST (ou do instance)
        status_val = None
        if self.is_bound:
            status_val = self.data.get(self.add_prefix("status"))
        if not status_val:
            status_val = self.instance.status

        if status_val != TermoSaida.STATUS_DEVOLVIDO:
            self.fields["data_devolucao"].disabled = True

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status") or self.instance.status

        if status == TermoSaida.STATUS_DEVOLVIDO:
            if not cleaned.get("data_devolucao"):
                self.add_error(
                    "data_devolucao", "Informe a data de devolução para status DEVOLVIDO."
                )
        else:
            cleaned["data_devolucao"] = None

        return cleaned
