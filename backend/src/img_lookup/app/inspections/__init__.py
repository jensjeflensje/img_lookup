from .metadata import MetadataInspection
from .place import PlaceInspection
from .properties import PropertiesInspection
from .vision import VisionInspection

INSPECTIONS = {
    "metadata": MetadataInspection,
    "place": PlaceInspection,
    "vision": VisionInspection,
    "properties": PropertiesInspection,
}