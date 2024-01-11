from django.conf import settings

from img_lookup.app.inspections.base import BaseInspection


class PlaceInspection(BaseInspection):
    def run(self, data: dict):
        import requests

        if not data.get("latitude") or not data.get("longitude"):
            return {}

        res = requests.get("http://api.positionstack.com/v1/reverse", params={
            "access_key": settings.POSITIONSTACK_KEY,
            "query": f"{data['latitude']},{data['longitude']}",
            "limit": 1
        })

        res.raise_for_status()

        res_json = res.json()

        if len(res_json["data"]) > 0:
            return res_json["data"][0]

        return dict({})
