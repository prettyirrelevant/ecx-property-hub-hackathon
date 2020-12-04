from django.urls import path

from . import views

urlpatterns = [
    path("mock/listings/", views.listings, name="all-listings"),
    path("mock/listings/<int:pk>/", views.listing, name="single-listing"),
    path("mock/listings/saved/", views.saved_listings, name="saved-listings"),
    path("mock/accounts/profile/agent/", views.agent_profile, name="agent-profile"),
    path("mock/accounts/profile/", views.profile, name="profile"),
]
