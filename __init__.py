"""
ComfyUI Image Rater Node
Custom node for rating and organizing images based on quality scores.
"""

from .nodes.image_rater import ImageRaterNode
from .nodes.image_organizer import ImageOrganizerNode

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "ImageRater": ImageRaterNode,
    "ImageOrganizer": ImageOrganizerNode,
}

# Human-readable node names
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRater": "Image Rater",
    "ImageOrganizer": "Image Organizer",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
