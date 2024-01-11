from img_lookup.app.models import Asset


class BaseInspection:
    def __init__(self, asset_id: str):
        self.asset_id = asset_id
        self.asset = Asset.objects.get(id=asset_id)

    def run(self, *args, **kwargs):
        raise NotImplementedError()
