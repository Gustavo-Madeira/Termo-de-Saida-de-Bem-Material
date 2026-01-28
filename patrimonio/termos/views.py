from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import EditarSaidaForm, RegistrarSaidaForm
from .models import TermoSaida


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url="login")(view_func)


def termo_list_publico(request):
    # Página inicial: SEM login
    termos = TermoSaida.objects.all()
    return render(request, "termo_list.html", {"termos": termos})


@admin_required
def registrar_saida(request):
    if request.method == "POST":
        form = RegistrarSaidaForm(request.POST)
        if form.is_valid():
            termo = form.save(commit=False)

            # Se informou data_devolucao, vira DEVOLVIDO; senão, ABERTO
            if termo.data_devolucao:
                termo.status = TermoSaida.STATUS_DEVOLVIDO
            else:
                termo.status = TermoSaida.STATUS_ABERTO

            termo.save()
            return redirect("termo_list")
    else:
        form = RegistrarSaidaForm()

    return render(request, "termo_form.html", {"form": form, "titulo": "Registrar Saída"})


@admin_required
def editar_saidas_list(request):
    # Tela de gerenciamento (admin) listando tudo com Editar/Excluir
    termos = TermoSaida.objects.all()
    return render(request, "termo_manage_list.html", {"termos": termos})


@admin_required
def editar_saida(request, pk: int):
    termo = get_object_or_404(TermoSaida, pk=pk)

    if request.method == "POST":
        form = EditarSaidaForm(request.POST, instance=termo)
        if form.is_valid():
            termo = form.save(commit=False)

            # Se status DEVOLVIDO e não tem data_devolucao, força data_devolucao hoje? (opcional)
            # Aqui vou só manter coerência simples:
            if termo.status == TermoSaida.STATUS_DEVOLVIDO and not termo.data_devolucao:
                # deixa em branco se você quiser permitir devolvido sem data
                pass

            if termo.data_devolucao:
                termo.status = TermoSaida.STATUS_DEVOLVIDO

            termo.save()
            return redirect("editar_saidas")
    else:
        form = EditarSaidaForm(instance=termo)

    return render(request, "termo_form.html", {"form": form, "titulo": "Editar Saída"})


@admin_required
@require_POST
def excluir_saida(request, pk: int):
    termo = get_object_or_404(TermoSaida, pk=pk)
    termo.delete()
    return redirect("editar_saidas")