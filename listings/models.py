import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
    SearchVectorField,
)
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from accounts.models import Agent, CustomUser


class ListingManager(models.Manager):
    # an attempt of making things nice
    def search(self, search_text):
        search_vectors = SearchVector(
            "name", weight="A", config="english"
        ) + SearchVector(
            StringAgg("description", delimiter=" "), weight="B", config="english"
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity("name", search_text)
        qs = (
            self.get_queryset()
                .filter(search_vector=search_query)
                .annotate(rank=search_rank + trigram_similarity)
                .order_by("-rank")
        )
        return qs


class Listing(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="listings", null=False
    )
    name = models.CharField(_("name"), max_length=150, blank=False, null=False)
    description = models.TextField(
        _("description"), blank=False, null=False, max_length=500
    )
    location = models.CharField(_("location"), max_length=100, blank=False, null=False)
    price = models.IntegerField(_("price"), null=False, blank=False)
    is_new = models.BooleanField(_("is_new"), default=False)
    is_furnished = models.BooleanField(_("is furnished"), default=False)
    likes = models.ManyToManyField(CustomUser, related_name="listing_likes")
    bedrooms = models.IntegerField(_("bedrooms"), default=0)
    bathrooms = models.IntegerField(_("bathrooms"), default=0)
    lounges = models.IntegerField(_("lounges"), default=0)
    created_on = models.DateTimeField(_("created_on"), auto_now_add=True)

    search_vector = SearchVectorField(null=True)

    objects = ListingManager()

    @property
    def no_of_likes(self) -> int:
        return self.likes.count()


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images", null=False
    )
    image_file = CloudinaryField("image")
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    @property
    def image_url(self):
        return f"https://res.cloudinary.com/dybhjquqy/{self.image_file}"


class Review(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="reviews", null=False
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews", null=False
    )
    message = models.CharField(_("message"), max_length=180, null=False, blank=False)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)


# delete image(s) from cloudinary on model's deletion
@receiver(pre_delete, sender=ListingImage)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image_field.public_id)


# update search_vector
@receiver(post_save, sender=Listing)
def update_search_vector(sender, instance, **kwargs):
    Listing.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("name", weight="A")
                      + SearchVector("description", weight="B")
    )
