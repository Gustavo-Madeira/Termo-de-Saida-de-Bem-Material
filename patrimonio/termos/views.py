from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import TermoSaida
from .forms import RegistrarSaidaForm, EditarSaidaForm


def termo_list_publico(request):
    termos = TermoSaida.objects.all()
    return render(request, "termo_list.html", {"termos": termos})


@login_required
def termo_manage_list(request):
    termos = TermoSaida.objects.all()
    return render(request, "termo_manage_list.html", {"termos": termos})


@login_required
def registrar_saida(request):
    if request.method == "POST":
        form = RegistrarSaidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RegistrarSaidaForm()

    return render(
        request,
        "termo_form.html",
        {"form": form, "titulo": "Registrar Saída"},
    )


@login_required
def editar_saida(request, pk):
    termo = get_object_or_404(TermoSaida, pk=pk)

    if request.method == "POST":
        form = EditarSaidaForm(request.POST, instance=termo)
        if form.is_valid():
            form.save()
            return redirect("termo_manage_list")
    else:
        form = EditarSaidaForm(instance=termo)

    return render(
        request,
        "termo_edit.html",
        {"form": form, "titulo": "Editar Saída"},
    )


@login_required
def excluir_saida(request, pk):
    termo = get_object_or_404(TermoSaida, pk=pk)
    if request.method == "POST":
        termo.delete()
    return redirect("termo_manage_list")
