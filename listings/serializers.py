from rest_framework import serializers

from accounts.serializers import AgentSerializer, UserSerializer
from .models import Listing, ListingImage, Review


class ListingImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = ListingImage
        fields = ("image_url",)


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "message", "timestamp")
        extra_kwargs = {"timestamp": {"read_only": True}}

    def create(self, validated_data):
        current_user = self.context.get("request").user
        listing = self.context.get("listing")

        validated_data.update({"listing": listing, "user": current_user})
        review = Review.objects.create(**validated_data)

        return review


class ListingSerializer(serializers.ModelSerializer):
    no_of_likes = serializers.ReadOnlyField()
    listing_images = ListingImageSerializer(many=True, read_only=True, source="images")
    agent = AgentSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = (
            "id",
            "agent",
            "name",
            "location",
            "description",
            "price",
            "is_new",
            "reviews",
            "bedrooms",
            "bathrooms",
            "lounges",
            "no_of_likes",
            "listing_images",
            "created_on",
        )
        extra_kwargs = {"created_on": {"read_only": True}}

    def create(self, validated_data):
        images_data = self.context.get("request").FILES
        current_user = self.context.get("request").user
        validated_data.update({"agent_id": current_user.agent.user_id})

        listing = Listing.objects.create(**validated_data)

        for image_data in images_data.getlist("file"):
            ListingImage.objects.create(listing=listing, image_file=image_data)

        return listing
