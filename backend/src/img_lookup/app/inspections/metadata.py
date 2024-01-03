from django.core.files.storage import default_storage
from django_q.tasks import async_task

from img_lookup.app.inspections.base import BaseInspection


class MetadataInspection(BaseInspection):


    def _gps_to_degrees(self, val):
        """
        Convert GPS data to decimal degrees, from the minute-second format.
        """
        if val is None:
            return None
        degrees, minutes, seconds = val.values
        return round(float(degrees + (minutes / 60) + (seconds / 3600)), 6)

    def _to_primitive(self, data):
        new_data = {}
        for key, val in data.items():
            if isinstance(val, dict):
                new_data[key] = self._to_primitive(val)
            elif isinstance(val, list):
                new_data[key] = []
                for item in val:
                    new_data[key].append(self._to_primitive(item))
            else:
                new_data[key] = str(val)
        return new_data

    def run(self):
        import exifread

        with default_storage.open(self.asset.file_key) as file:
            exif_data = exifread.process_file(file)

        # calculated values that are somewhat human-readable
        cleaned_data = {}

        if exif_data.get("GPS GPSLatitudeRef") is not None and exif_data.get("GPS GPSLongitudeRef") is not None:
            # support negative values
            lat_factor = 1 if exif_data.get("GPS GPSLatitudeRef").values[0] == "N" else -1
            long_factor = 1 if exif_data.get("GPS GPSLongitudeRef").values[0] == "E" else -1
            cleaned_data["latitude"] = self._gps_to_degrees(exif_data.get("GPS GPSLatitude")) * lat_factor
            cleaned_data["longitude"] = self._gps_to_degrees(exif_data.get("GPS GPSLongitude")) * long_factor

        if device := exif_data.get("Image Model"):
            cleaned_data["device"] = str(device)

        from img_lookup.app.tasks import run_inspection # to fix circular import
        async_task(run_inspection, self.asset_id, "place", data=cleaned_data)

        return dict({"exif": self._to_primitive(exif_data), "cleaned": cleaned_data})
