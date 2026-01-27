from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("novo/", views.termo_novo, name="termo_novo"),
]
