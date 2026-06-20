"""
Image Organizer Node
Organizes rated images into folders based on their ratings.
"""

import os
import shutil
import torch
from PIL import Image
import numpy as np

class ImageOrganizerNode:
    """
    Organizes images into folders based on rating scores.
    
    Folder structure:
    output/rated/
    ├── excellent/ (8-10)
    ├── good/ (5-7)
    ├── acceptable/ (3-4)
    └── rejected/ (1-2)
    """
    
    CATEGORY = "utils/rating"
    FUNCTION = "organize_images"
    RETURN_NAMES = ("organized_paths", "moved_count", "status")
    RETURN_TYPES = ("STRING", "INT", "STRING")
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "rating_scores": ("FLOAT",),
                "output_dir": ("STRING", {"default": "./output/rated"}),
            },
            "optional": {
                "categories": ("STRING", {"multiline": True, 
                    "default": "excellent:8-10\ngood:5-7\nacceptable:3-4\nrejected:1-2"}),
                "copy_mode": (["move", "copy"],),
                "filename_prefix": ("STRING", {"default": "rated"}),
            }
        }
    
    def organize_images(self, images, rating_scores, output_dir="./output/rated",
                       categories="excellent:8-10\ngood:5-7\nacceptable:3-4\nrejected:1-2",
                       copy_mode="move", filename_prefix="rated"):
        """
        Organize images into folders based on ratings.
        
        Args:
            images: Tensor of images
            rating_scores: Tensor of rating scores
            output_dir: Base output directory
            categories: Category definitions (name:min-max per line)
            copy_mode: 'move' or 'copy'
            filename_prefix: Prefix for saved filenames
            
        Returns:
            Tuple of (paths, count, status_message)
        """
        
        # Parse categories
        category_map = self._parse_categories(categories)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        moved_count = 0
        organized_paths = []
        status_messages = []
        
        # Convert scores to list if tensor
        if isinstance(rating_scores, torch.Tensor):
            scores = rating_scores.cpu().numpy().tolist()
        else:
            scores = rating_scores if isinstance(rating_scores, list) else [rating_scores]
        
        # Process each image
        for i, (img_tensor, score) in enumerate(zip(images, scores)):
            # Determine category
            category = self._get_category(score, category_map)
            category_dir = os.path.join(output_dir, category)
            
            # Create category directory
            os.makedirs(category_dir, exist_ok=True)
            
            # Convert tensor to image and save
            img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            img_pil = Image.fromarray(img_np)
            
            # Generate filename
            filename = f"{filename_prefix}_{category}_{i}_score{score:.1f}.png"
            filepath = os.path.join(category_dir, filename)
            
            # Save image
            img_pil.save(filepath)
            organized_paths.append(filepath)
            moved_count += 1
            
            status_messages.append(f"✓ {filename} -> {category}/ (score: {score:.1f})")
        
        status = f"Organized {moved_count} images into {len(set([os.path.dirname(p) for p in organized_paths]))} categories"
        paths_str = "\n".join(organized_paths)
        
        print(f"[ImageOrganizer] {status}")
        for msg in status_messages:
            print(f"[ImageOrganizer] {msg}")
        
        return (paths_str, moved_count, status)
    
    def _parse_categories(self, categories_str):
        """
        Parse category definitions from string.
        Format: "name:min-max" per line
        """
        category_map = {}
        
        for line in categories_str.strip().split('\n'):
            if ':' not in line:
                continue
            
            name, range_str = line.split(':', 1)
            name = name.strip()
            
            try:
                min_score, max_score = map(float, range_str.replace('-', ':').split(':'))
                category_map[name] = (min_score, max_score)
            except ValueError:
                print(f"[ImageOrganizer] Invalid category format: {line}")
        
        # Default categories if none parsed
        if not category_map:
            category_map = {
                "excellent": (8.0, 10.0),
                "good": (5.0, 7.9),
                "acceptable": (3.0, 4.9),
                "rejected": (1.0, 2.9)
            }
        
        return category_map
    
    def _get_category(self, score, category_map):
        """
        Get category name for a given score.
        """
        for name, (min_score, max_score) in category_map.items():
            if min_score <= score <= max_score:
                return name
        
        # Default to 'rejected' if no category matches
        return "rejected"
