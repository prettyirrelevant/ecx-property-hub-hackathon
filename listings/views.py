from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from accounts.permission import CustomIsAuthenticated
from .models import Listing
from .permission import AgentOnly, UserOnly, OwnerOnly
from .serializers import ListingSerializer, ReviewSerializer


class AddListingView(generics.CreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing
    parser_classes = (MultiPartParser,)
    permission_classes = [CustomIsAuthenticated, AgentOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "Listing created successfully!"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class AllListingsView(generics.ListAPIView):
    """
    For filtering results...
    e.g https://ecx-property-hub.herokuapp.com/?price=100000&is_furnished=1
    price: For 1m+, pass 1000001 as query value e.g price=1000001
    bathrooms: For 4+ bathrooms, pass 5 as query value e.g bathrooms=5
    bedrooms: For 4+ bedrooms, pass 5 as query value e.g bedrooms=5
    is_furnished: Pass 1 or 0 to represent value
    """
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()

    # filter result
    def get_queryset(self):
        queries = self.request.query_params
        if len(queries) < 1:
            return self.queryset.all()
        else:
            model = self.queryset.all()
            price = queries.get('price', None)
            bedrooms = queries.get('bedrooms', None)
            bathrooms = queries.get('bathrooms', None)
            is_furnished = queries.get('is_furnished', None)

            if price and price != 'Any':
                if price > 1000000:
                    model.filter(price__gte=price)
                else:
                    model.filter(price__lte=price)

            if bedrooms and bedrooms != 'Any':
                if bedrooms > 5:
                    model.filter(bedrooms__gte=bedrooms)
                else:
                    model.filter(bedrooms__lte=bedrooms)

            if bathrooms and bathrooms != 'Any':
                if bathrooms > 5:
                    model.filter(bathrooms__gte=bathrooms)
                else:
                    model.filter(bathrooms__lte=bathrooms)

            if is_furnished and is_furnished != 'Any':
                model.filter(is_furnished=bool(is_furnished))


class SingleListingView(generics.RetrieveAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()


class DestroyListingView(generics.DestroyAPIView):
    queryset = Listing
    serializer_class = ListingSerializer
    permission_classes = [CustomIsAuthenticated, AgentOnly, OwnerOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Listing deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SavedListingsView(generics.ListAPIView):
    permission_classes = [CustomIsAuthenticated]
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()

    def get_queryset(self):
        return self.request.user.listing_likes.all()


@api_view(["POST"])
@permission_classes([CustomIsAuthenticated])
def save_listing(request, pk):
    listing = get_object_or_404(Listing, id=pk)

    # check if listing has been saved already
    if listing.likes.filter(id=request.user.id).exists():
        return Response(
            {"detail": "You already saved this listing"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    listing.likes.add(request.user)
    return Response(
        {"detail": "Listing saved successfully"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([CustomIsAuthenticated])
def unsave_listing(request, pk):
    listing = get_object_or_404(Listing, id=pk)

    # check if listing has been saved already
    if not listing.likes.filter(id=request.user.id).exists():
        return Response(
            {"detail": "This listing has not been saved"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    listing.likes.add(request.user)
    return Response(
        {"detail": "Listing removed from saved successfully"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([CustomIsAuthenticated, UserOnly])
def add_review(request, pk):
    """
    Sample request:
    {
        "message": "I think this apartment is a scam"
    }
    """
    # get the listing instance
    listing = get_object_or_404(Listing, id=pk)

    serializer = ReviewSerializer(
        data=request.data, context={"request": request, "listing": listing}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {"detail": "Review added successfully!"}, status=status.HTTP_201_CREATED
    )


class SearchListingView(generics.ListAPIView):
    """
    Example: https://ecx-property-hub.herokuapp.com/api/listings/search/?q=two+bedroom+flat
    """
    serializer_class = ListingSerializer
    queryset = Listing

    def get_queryset(self):
        search_query = self.request.query_params.get("q", None)
        qs = self.queryset.objects.search(search_query)
        return qs
