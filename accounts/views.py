from smtplib import SMTPException

from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .mail import send_confirmation_email
from .models import CustomUser
from .permission import CustomIsAuthenticated
from .serializers import (
    UserSerializer,
    AgentSerializer,
    ResendEmailSerializer,
    ConfirmAccountSeriailzer,
)


class AgentRegistrationView(generics.CreateAPIView):
    """
    API endpoint for agent registration
    """

    serializer_class = AgentSerializer
    queryset = CustomUser

    def get_serializer_context(self):
        context = super(AgentRegistrationView, self).get_serializer_context()
        context.update({"is_agent": True})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        send_confirmation_email(serializer.data["user"])()

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "detail": "Account created succesfully! Please confirm your email",
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class RegistrationView(generics.CreateAPIView):
    """
    API endpoint for regular user registration
    """

    serializer_class = UserSerializer
    queryset = CustomUser

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        try:
            send_confirmation_email(serializer.data)
        except Exception:
            return Response(
                {
                    "detail": "Something went wrong but account creation was successful! Please request confirmation "
                              "code again",
                    "email": serializer.data["email"],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "detail": "Account created succesfully! Please confirm your email",
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ObtainTokenView(ObtainAuthToken):
    """
    API endpoint for obtaining token for authentication
    """

    pass


class ResendConfirmationView(generics.GenericAPIView):
    serializer_class = ResendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Handle cases where email does not exist
        try:
            user = CustomUser.objects.get(email=serializer.data["email"])
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "No account exists with such email address"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serialized_user = UserSerializer(user).data

        # check if the account has been confirmed already
        if user.is_confirmed:
            return Response(
                {"detail": "Email address has already been confirmed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if the mail was sent successfully
        try:
            send_confirmation_email(serialized_user)
        except SMTPException:
            # TODO decide whether to remove the email
            return Response(
                {
                    "detail": "Something went wrong! Please request confirmation code again",
                    "email": serializer.data["email"],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            return Response(
                {"detail": "Confirmation code sent to email address successfully"},
                status=status.HTTP_200_OK,
            )


class ConfirmAccountView(generics.GenericAPIView):
    serializer_class = ConfirmAccountSeriailzer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Handle cases where confirmation code is not attached to an account
        try:
            user = CustomUser.objects.get(
                confirmation_code=serializer.data["confirmation_code"]
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User account does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # handle cases where account is already confirmed
        if user.is_confirmed:
            return Response(
                {"detail": "User account already confirmed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # confirm account
        user.is_confirmed = True
        user.save()

        return Response(
            {"detail": "Account confirmed successfully!"}, status=status.HTTP_200_OK
        )


class ProfileView(generics.GenericAPIView):
    """
    Endpoint that returns the details about the currently logged in user
    """

    serializer_class = UserSerializer
    permission_classes = [CustomIsAuthenticated]

    # return separate serializer based on account type
    def get_serializer_class(self):
        if not self.request.user.is_anonymous and self.request.user.is_agent:
            return AgentSerializer

        return self.serializer_class

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_agent:
            serializer = self.get_serializer(instance=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(instance=request.user.agent)
            return Response(serializer.data, status=status.HTTP_200_OK)
