from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import TermoSaida, ItemTermo
from .forms import RegistrarSaidaForm


@login_required
def home(request):
    termos = TermoSaida.objects.order_by("-criado_em")
    return render(request, "termo_list.html", {"termos": termos})


@login_required
def termo_novo(request):
    if request.method == "POST":
        form = RegistrarSaidaForm(request.POST)
        if form.is_valid():
            # cria o termo
            termo = form.save(commit=False)
            termo.criado_por = request.user
            termo.save()

            # cria o item (produto/bem) atrelado ao termo
            ItemTermo.objects.create(
                termo=termo,
                patrimonio_num=form.cleaned_data["patrimonio_num"],
                descricao_bem=form.cleaned_data["descricao_bem"],
                assinatura_retirada=form.cleaned_data["responsavel_nome"],  # opcional
            )

            return redirect("home")
    else:
        form = RegistrarSaidaForm()

    return render(request, "termo_forma.html", {"form": form})
