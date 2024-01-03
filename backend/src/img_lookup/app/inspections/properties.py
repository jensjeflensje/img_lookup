import hashlib

from django.core.files.storage import default_storage
from django_q.tasks import async_task

from PIL import Image, ImageOps

from img_lookup.app.inspections.base import BaseInspection


class PropertiesInspection(BaseInspection):

    def run(self):

        with default_storage.open(self.asset.file_key) as file:
            image = Image.open(file)
        old_size = image.size
        image = ImageOps.exif_transpose(image)

        orientation_diff = image.size != old_size
        width, height = image.size

        img_bytes = image.tobytes()
        md5_hash = hashlib.md5(img_bytes)
        sha256_hash = hashlib.sha256(img_bytes)

        self.asset.width = width
        self.asset.height = height
        self.asset.orientation_diff = orientation_diff
        self.asset.save()

        from img_lookup.app.tasks import run_inspection # to fix circular import
        async_task(run_inspection, self.asset.id, "vision")

        return dict({
            "width": width,
            "height": height,
            "hash": {
                "md5": md5_hash.hexdigest(),
                "sha256": sha256_hash.hexdigest()
            }
        })
