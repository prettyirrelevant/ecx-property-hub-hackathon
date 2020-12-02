from django.urls import path

from . import views

urlpatterns = [
    path("listings/<int:pk>/add_review/", views.add_review, name="add-review"),
    path("listings/saved/", views.SavedListingsView.as_view(), name="saved-listings"),
    path("listings/<int:pk>/save/", views.save_listing, name="add-listing-to-saved"),
    path(
        "listings/<int:pk>/unsave/",
        views.unsave_listing,
        name="remove-listing-from-saved",
    ),
    path("listings/create/", views.AddListingView.as_view(), name="create-listing"),
    path("listings/", views.AllListingsView.as_view(), name="all-listings"),
    path(
        "listings/<int:pk>/",
        views.SingleListingView.as_view(),
        name="single-listing",
    ),
    path(
        "listings/<int:pk>/delete/",
        views.DestroyListingView.as_view(),
        name="delete-listing",
    ),
    path("listings/search/", views.SearchListingView.as_view(), name="search-listing"),
]
