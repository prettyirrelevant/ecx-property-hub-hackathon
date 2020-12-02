from django.urls import path

from . import views

urlpatterns = [
    path(
        "accounts/register/", views.RegistrationView.as_view(), name="registration"
    ),
    path(
        "accounts/register/agent/",
        views.AgentRegistrationView.as_view(),
        name="agent-registration",
    ),
    path(
        "accounts/request_token/", views.ObtainTokenView.as_view(), name="obtain-token"
    ),
    path(
        "accounts/resend_confirmation/",
        views.ResendConfirmationView.as_view(),
        name="resend-confirmation",
    ),
    path(
        "accounts/confirm/",
        views.ConfirmAccountView.as_view(),
        name="confirm-account",
    ),
    path("accounts/profile/", views.ProfileView.as_view(), name="my-profile"),
]
