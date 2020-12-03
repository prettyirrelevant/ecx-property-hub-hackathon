from mimesis.schema import Field, Schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

_ = Field("en")


@api_view(["GET"])
def listings(request):
    schema = Schema(
        schema=lambda: {
            "id": _("uuid"),
            "name": _("text.sentence"),
            "description": _("text"),
            "is_furnished": _("development.boolean"),
            "is_new": _("development.boolean"),
            "bedrooms": _("numbers.integer_number", start=0, end=6),
            "bathrooms": _("numbers.integer_number", start=0, end=8),
            "no_of_likes": _("numbers.integer_number", start=0, end=100),
            "location": _("address"),
            "listing_images": [
                {"image_url": _("person.avatar")},
                {"image_url": _("person.avatar")},
                {"image_url": _("person.avatar")},
            ],
            "created_on": _("timestamp", posix=False),
            "agent": {
                "user": {
                    "email": _("person.email", domains=["test.com"], key=str.lower),
                    "first_name": _("person.name"),
                    "last_name": _("person.surname"),
                    "image_url": _("person.avatar"),
                },
                "phone_number": _("person.telephone"),
                "agent_display_name": _("business.company"),
            },
        }
    )

    data = schema.create(iterations=int(request.query_params.get("l", 10)))
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def saved_listings(request):
    schema = Schema(
        schema=lambda: {
            "id": _("uuid"),
            "name": _("text.sentence"),
            "description": _("text"),
            "is_furnished": _("development.boolean"),
            "is_new": _("development.boolean"),
            "bedrooms": _("numbers.integer_number", start=0, end=6),
            "bathrooms": _("numbers.integer_number", start=0, end=8),
            "no_of_likes": _("numbers.integer_number", start=0, end=100),
            "location": _("address"),
            "listing_images": [
                {"image_url": _("person.avatar")},
                {"image_url": _("person.avatar")},
                {"image_url": _("person.avatar")},
            ],
            "created_on": _("timestamp", posix=False),
            "agent": {
                "user": {
                    "email": _("person.email", domains=["test.com"], key=str.lower),
                    "first_name": _("person.name"),
                    "last_name": _("person.surname"),
                    "image_url": _("person.avatar"),
                    "date_joined": _("timestamp", posix=False),
                },
                "phone_number": _("person.telephone"),
                "agent_display_name": _("business.company"),
            },
        }
    )

    data = schema.create(iterations=int(request.query_params.get("l", 5)))
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def agent_profile(request):
    schema = Schema(
        schema=lambda: {
            "user": {
                "email": _("person.email", domains=["test.com"], key=str.lower),
                "first_name": _("person.name"),
                "last_name": _("person.surname"),
                "image_url": _("person.avatar"),
                "date_joined": _("timestamp", posix=False),
            },
            "phone_number": _("person.telephone"),
            "agent_display_name": _("business.company"),
        }
    )

    data = schema.create()
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def profile(request):
    schema = Schema(
        schema=lambda: {
            "email": _("person.email", domains=["test.com"], key=str.lower),
            "first_name": _("person.name"),
            "last_name": _("person.surname"),
            "image_url": _("person.avatar"),
            "date_joined": _("timestamp", posix=False),
        }
    )

    data = schema.create()
    return Response(data, status=status.HTTP_200_OK)
