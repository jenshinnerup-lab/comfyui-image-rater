"""
ComfyUI Image Rater
Custom node for rating and organizing images based on quality scores.
"""

from .nodes.image_rater import ImageRaterNode
from .nodes.image_organizer import ImageOrganizerNode
from .nodes.batch_rater import BatchImageRaterNode

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "ImageRater": ImageRaterNode,
    "ImageOrganizer": ImageOrganizerNode,
    "BatchImageRater": BatchImageRaterNode,
}

# Human-readable node names
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRater": "Image Rater",
    "ImageOrganizer": "Image Organizer",
    "BatchImageRater": "Batch Image Rater (Asset Page)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
