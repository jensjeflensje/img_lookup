import requests
from django.conf import settings
from google.cloud import vision
from google.protobuf.json_format import MessageToDict


from img_lookup.app.inspections.base import BaseInspection
from img_lookup.app.utils import s3_generate_presigned_get


def analyze_image_from_uri(
    image_uri: str,
    feature_types,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.content = requests.get(image_uri).content
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)

    return response


class VisionInspection(BaseInspection):

    def run(self):
        get_url = s3_generate_presigned_get(self.asset.file_key)
        response = analyze_image_from_uri(get_url, [
            vision.Feature.Type.TEXT_DETECTION,
            vision.Feature.Type.WEB_DETECTION,
            vision.Feature.Type.LANDMARK_DETECTION,
        ])

        words = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        if len(word.symbols) < 3: continue # filter out gibberish
                        vertices = MessageToDict(word.bounding_box._pb)["vertices"]
                        if self.asset.orientation_diff: # exif data might differ from image channel length
                            vertices = [{"x": self.asset.width - vertice["y"], "y": vertice["x"]} for vertice in vertices]

                        word_obj = {
                            "text": "".join([symbol.text for symbol in word.symbols]),
                            "vertices": vertices,
                        }
                        if len(word.property.detected_languages) > 0:
                            word_obj["language_code"] = word.property.detected_languages[0].language_code
                            word_obj["language_name"] = settings.LANGUAGES.get(word_obj["language_code"])
                        words.append(word_obj)

        landmarks = []
        for landmark in response.landmark_annotations:
            landmark_obj = {
                "name": landmark.description,
            }
            if len(landmark.locations) > 0:
                landmark_obj["location"] = MessageToDict(landmark.locations[0]._pb).get("latLng")
            landmarks.append(landmark_obj)

        keywords = []
        for entity in response.web_detection.web_entities:
            if entity.score < 0.5: continue
            keywords.append(entity.description)

        labels = [] # labels are better than keywords
        for label in response.web_detection.best_guess_labels:
            labels.append(label.label)

        pages = []
        for page in response.web_detection.pages_with_matching_images:
            pages.append({
                "name": page.page_title,
                "url": page.url,
            })

        return dict({
            "words": words,
            "landmarks": landmarks,
            "keywords": keywords,
            "labels": labels,
            "pages": pages,
        })
