import requests
from django.conf import settings
from django.http import Http404
from django_q.tasks import async_task
from rest_framework.exceptions import ValidationError

from img_lookup.app.tasks import run_inspection
from img_lookup.app.models import Asset
from img_lookup.app.serializers import CreateAssetUploadSerializer, AssetUploadSerializer
from img_lookup.app.utils import s3_generate_presigned_put, s3_key_exists
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class CreateAssetUploadEndpoint(GenericAPIView):
    def post(self, request):
        serializer = CreateAssetUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset = serializer.save()
        url = s3_generate_presigned_put(asset.file_key, asset.content_type)

        return Response({"url": url, "id": asset.id})


class BaseAssetDetailEndpoint(GenericAPIView):
    queryset = Asset.objects.filter(is_available=True)
    lookup_field = 'id'

    def get_object(self):
        asset = super().get_object()
        if not s3_key_exists(asset.file_key):
            raise ValidationError("There is no file associated with this asset")
        return asset


class GetAssetUploadEndpoint(BaseAssetDetailEndpoint):

    def get(self, request, id):
        asset = self.get_object()
        serializer = AssetUploadSerializer(instance=asset)
        return Response(serializer.data)


class ExtendAssetLifetimeEndpoint(BaseAssetDetailEndpoint):

    def post(self, request, id):
        asset = self.get_object()
        if asset.is_extended:
            raise ValidationError("This asset's lifetime has already been extended")

        asset.expires_at = asset.created_at + settings.EXTENDED_ASSET_EXPIRY
        asset.is_extended = True
        asset.save()

        serializer = AssetUploadSerializer(instance=asset)
        return Response(serializer.data)


class FinalizeAssetUploadEndpoint(BaseAssetDetailEndpoint):
    queryset = Asset.objects.filter(is_available=False)

    def post(self, request, id):
        asset = self.get_object()
        asset.is_available = True
        asset.save()

        for inspection in settings.INITIAL_INSPECTIONS:
            # initial inspections will trigger all other inspections when they're done
            async_task(run_inspection, asset.id, inspection)

        return Response({"inspections": settings.ALL_INSPECTIONS})
    

class GetAssetInspectionEndpoint(GenericAPIView):
    lookup_field = 'inspection_type'

    def get_queryset(self):
        return Asset.objects.get(id=self.kwargs['id']).inspections

    def get(self, request, id, inspection_type):
        try:
            inspection = self.get_object()
        except Http404:  # convert 404 to 202 as it's still processing
            return Response({"info": "Inspection in progress"}, status=status.HTTP_202_ACCEPTED)
        
        return Response(inspection.data)


class FetchMarktplaatsEndpoint(GenericAPIView):
    def get(self, request):
        url = request.query_params.get('url')
        ad_id = url.split('/')[-1].split('-')[0]

        search_res = requests.get("https://www.marktplaats.nl/lrp/api/search", params={
            "query": ad_id,
            "limit": 1,
        }).json()

        listings = search_res['listings']
        if len(listings) < 1:
            return Response(status=status.HTTP_404_NOT_FOUND)

        listing = listings[0]

        location = listing['location']
        lat = location.get('latitude')
        lng = location.get('longitude')

        zip_res = requests.get("http://api.positionstack.com/v1/reverse", params={
            "access_key": settings.POSITIONSTACK_KEY,
            "query": f"{lat},{lng}",
            "limit": 1
        }).json()['data'][0]

        return Response({
            "name": listing['title'],
            "author": listing['sellerInformation']['sellerName'],
            "latitude": lat,
            "longitude": lng,
            "zipCode": zip_res['postal_code'],
        })
