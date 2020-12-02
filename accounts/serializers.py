from rest_framework import serializers

from .models import CustomUser, Agent


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "image_url",
            "is_customer",
            "confirmation_code",
            "is_confirmed",
            "is_agent",
            "date_joined",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
            "is_agent": {"read_only": True},
            "is_customer": {"read_only": True},
            "is_confirmed": {"read_only": True},
            "confirmation_code": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data.update({"is_customer": True})
        user = CustomUser.objects.create_user(**validated_data)
        return user


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Agent
        fields = ("user", "phone_number", "agent_display_name")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"is_agent": True})
        user = CustomUser.objects.create_user(**user_data)
        agent = Agent.objects.create(user=user, **validated_data)
        return agent


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmAccountSeriailzer(serializers.Serializer):
    confirmation_code = serializers.IntegerField(required=True)
