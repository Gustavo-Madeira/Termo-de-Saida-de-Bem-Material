from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrarSaidaForm, TermoEditForm
from .models import TermoSaida


def termo_list_publico(request):
    termos = TermoSaida.objects.all()
    return render(request, "termo_list.html", {"termos": termos})


@login_required
def registrar_saida(request):
    if request.method == "POST":
        form = RegistrarSaidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("termo_list_publico")
    else:
        form = RegistrarSaidaForm()

    # Mantive o nome do seu template como está: termo_form.html
    return render(request, "termo_form.html", {"form": form, "titulo": "Registrar Saída"})


@login_required
def editar_list(request):
    termos = TermoSaida.objects.all()
    return render(request, "termo_manage_list.html", {"termos": termos})


@login_required
def editar_saida(request, pk: int):
    termo = get_object_or_404(TermoSaida, pk=pk)

    if request.method == "POST":
        form = TermoEditForm(request.POST, instance=termo)
        if form.is_valid():
            form.save()
            return redirect("editar_list")
    else:
        form = TermoEditForm(instance=termo)

    return render(request, "termo_edit.html", {"form": form, "termo": termo})


@login_required
def excluir_saida(request, pk: int):
    termo = get_object_or_404(TermoSaida, pk=pk)
    if request.method == "POST":
        termo.delete()
    return redirect("editar_list")
