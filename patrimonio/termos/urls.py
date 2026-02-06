from django.urls import path
from . import views

urlpatterns = [
    path("", views.termo_list_publico, name="home"),
    path("registrar/", views.registrar_saida, name="registrar_saida"),
    path("editar/", views.termo_manage_list, name="termo_manage_list"),
    path("editar/<int:pk>/", views.editar_saida, name="editar_saida"),
    path("excluir/<int:pk>/", views.excluir_saida, name="excluir_saida"),
]
