from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # rotas do app
    path("", include("termos.urls")),

    # rotas prontas do Django Auth: /login/ /logout/ etc
    path("", include("django.contrib.auth.urls")),
]
