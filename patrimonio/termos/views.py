from functools import wraps
from urllib.parse import urlencode

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EditarSaidaForm, RegistrarSaidaForm
from .models import TermoSaida


ADMIN_TAB_SESSION_KEY = "admin_tab_token"


def admin_tab_required(view_func):
    """
    Exige:
    - usuário logado
    - usuário superuser
    - token ?tab=... (vem do sessionStorage, some ao fechar a aba)

    Isso faz:
    - Fechou a ABA -> sessionStorage perde o tab -> ao clicar de novo gera outro tab -> força login
    - Fechou o NAVEGADOR -> cookie de sessão morre (SESSION_EXPIRE_AT_BROWSER_CLOSE=True) -> força login
    """

    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        # Só admin
        if not request.user.is_superuser:
            logout(request)
            return redirect("login")

        token = request.GET.get("tab") or request.POST.get("tab")
        if not token:
            # sem token de aba: joga pro público (e o clique correto gera o tab)
            return redirect("home")

        bound = request.session.get(ADMIN_TAB_SESSION_KEY)

        # Se já estava preso a outra aba, desloga e força login
        if bound and bound != token:
            logout(request)
            next_url = request.get_full_path()
            login_url = reverse("login") + "?" + urlencode({"next": next_url})
            return redirect(login_url)

        # Prende a sessão a esta aba
        request.session[ADMIN_TAB_SESSION_KEY] = token
        return view_func(request, *args, **kwargs)

    return _wrapped


def termo_list_publico(request):
    termos = TermoSaida.objects.all().order_by("-data_retirada", "-criado_em")
    return render(request, "termo_list.html", {"termos": termos})


@admin_tab_required
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
        {"form": form, "titulo": "Registrar Saída", "modo": "registrar"},
    )


@admin_tab_required
def termo_manage_list(request):
    termos = TermoSaida.objects.all().order_by("-data_retirada", "-criado_em")
    return render(request, "termo_manage_list.html", {"termos": termos})


@admin_tab_required
def editar_saida(request, pk: int):
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
        {"form": form, "termo": termo, "titulo": "Editar Saída"},
    )


@admin_tab_required
def excluir_saida(request, pk: int):
    termo = get_object_or_404(TermoSaida, pk=pk)
    if request.method == "POST":
        termo.delete()
    return redirect("termo_manage_list")
