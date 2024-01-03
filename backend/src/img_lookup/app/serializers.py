from datetime import datetime, timedelta
import uuid

from django.conf import settings
from img_lookup.app.models import Asset
from img_lookup.app.utils import get_file_extension, s3_generate_presigned_get
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class CreateAssetUploadSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField()
    content_type = serializers.CharField()
    
    def validate(self, data):
        if get_file_extension(data["file_name"]) not in settings.ACCEPTED_FILE_TYPES:
            raise ValidationError("File extension isn't supported.")
        
        asset_id = uuid.uuid4()
        data.update({
            "id": asset_id,
            "file_key": f"{settings.INPUTS_FOLDER}/{asset_id}.{get_file_extension(data['file_name'])}",
            "expires_at": datetime.now() + settings.ASSET_EXPIRY,
        })

        return data
    
    class Meta:
        fields = ('file_name', 'content_type', )
        model = Asset


class AssetUploadSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField()
    url = serializers.SerializerMethodField() # S3 presigned url

    def get_url(self, obj):
        return s3_generate_presigned_get(obj.file_key)

    class Meta:
        fields = ('id', 'file_name', 'url', 'is_extended', 'expires_at')
        model = Asset