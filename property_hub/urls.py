from django.shortcuts import redirect
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


def index(request):
    return redirect("redoc/")


schema_view = get_schema_view(
    openapi.Info(
        title="Property Hub",
        default_version="v1",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("", index, name="index"),
    path("api/", include("accounts.urls")),
    path("api/", include("listings.urls")),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
