from django.urls import path
from . import views

urlpatterns = [
    path("", views.termo_list_publico, name="termo_list_publico"),

    path("registrar/", views.registrar_saida, name="registrar_saida"),
    path("editar/", views.editar_list, name="editar_list"),
    path("editar/<int:pk>/", views.editar_saida, name="editar_saida"),
    path("excluir/<int:pk>/", views.excluir_saida, name="excluir_saida"),
]
