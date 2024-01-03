import uuid
from django.db import models

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, editable=False) # will be set inside the serializer
    file_name = models.TextField(blank=False, null=False)
    file_key = models.TextField(blank=False, null=False)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    orientation_diff = models.BooleanField(default=False)
    content_type = models.TextField(blank=False, null=False)
    is_available = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    is_extended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("file_key", name="unique_file_key"),
        ]


class AssetInspection(models.Model):
    class InspectionType(models.TextChoices):
        VISION = "vision"
        METADATA = "metadata"
        PLACE = "place"

    asset = models.ForeignKey(Asset, related_name="inspections", on_delete=models.CASCADE)
    inspection_type = models.TextField(choices=InspectionType.choices, null=False, blank=False)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("asset", "inspection_type", name="unique_asset_inspection_type"),
        ]
