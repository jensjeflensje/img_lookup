from django.utils import timezone

from img_lookup.app.models import Asset
from img_lookup.app.inspections import INSPECTIONS
from img_lookup.app.utils import s3_remove_object


def run_inspection(asset_id: str, inspection_type: str, *args, **kwargs):
    inspection = INSPECTIONS.get(inspection_type)(asset_id)
    result = inspection.run(*args, **kwargs)
    
    asset = Asset.objects.get(id=asset_id)
    asset.inspections.create(inspection_type=inspection_type, data=result)

def clean_up_assets():
    for asset in Asset.objects.filter(expires_at__lt=timezone.now()):
        s3_remove_object(asset.file_key)
        asset.delete()
