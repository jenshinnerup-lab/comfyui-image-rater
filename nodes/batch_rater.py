"""
Batch Image Rater Node
Rates all images in a directory and optionally organizes them.

This node is designed for the Asset Page use case - 
processing existing batches of generated images.
"""

import os
import torch
import numpy as np
from PIL import Image
import folder_paths

class BatchImageRaterNode:
    """
    Scan a directory, rate all images, and organize by score.
    
    Perfect for asset pages where you want to:
    - Rate existing batches
    - Sort by quality
    - Move best images to showcase folders
    """
    
    CATEGORY = "utils/rating"
    FUNCTION = "rate_batch"
    RETURN_NAMES = ("rated_images", "scores", "paths", "summary")
    RETURN_TYPES = ("IMAGE", "FLOAT", "STRING", "STRING")
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        # Get ComfyUI's standard input/output directories
        input_dirs = folder_paths.get_directory_by_type("input")
        output_dirs = folder_paths.get_directory_by_type("output")
        
        return {
            "required": {
                "source_directory": ("STRING", {
                    "default": "./output",
                    "multiline": False
                }),
                "file_pattern": ("STRING", {
                    "default": "*.png",
                    "multiline": False,
                    "placeholder": "*.png, *.jpg, etc."
                }),
                "rating_method": (["heuristic", "blur_detection", "contrast", "combined"],),
            },
            "optional": {
                "min_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "organize_by_score": ("BOOLEAN", {"default": True}),
                "output_base": ("STRING", {"default": "./output/rated"}),
                "categories": ("STRING", {
                    "multiline": True,
                    "default": "excellent:8-10\ngood:5-7\nacceptable:3-4\nrejected:1-2"
                }),
                "copy_mode": (["move", "copy", "keep_original"],),
                "filename_with_score": ("BOOLEAN", {"default": True}),
            }
        }
    
    def rate_batch(self, source_directory, file_pattern="*.png", rating_method="heuristic",
                   min_score=0.0, organize_by_score=True, output_base="./output/rated",
                   categories="excellent:8-10\ngood:5-7\nacceptable:3-4\nrejected:1-2",
                   copy_mode="move", filename_with_score=True):
        """
        Process all images in directory.
        """
        import glob
        import cv2
        
        # Resolve relative paths from ComfyUI root
        if not os.path.isabs(source_directory):
            source_directory = os.path.join(folder_paths.get_output_directory(), source_directory.lstrip('./'))
        
        # Find all matching images
        pattern = os.path.join(source_directory, file_pattern)
        image_files = glob.glob(pattern)
        
        # Also check subdirectories
        if not image_files:
            pattern = os.path.join(source_directory, "**", file_pattern)
            image_files = glob.glob(pattern, recursive=True)
        
        if not image_files:
            return (torch.zeros(1), torch.zeros(1), "No images found", 
                   f"❌ No images found matching: {file_pattern}")
        
        print(f"[BatchImageRater] Found {len(image_files)} images in {source_directory}")
        
        # Process each image
        rated_images = []
        scores = []
        paths = []
        summary_data = {
            "total": 0,
            "rated": 0,
            "excellent": 0,
            "good": 0,
            "acceptable": 0,
            "rejected": 0,
            "errors": 0
        }
        
        category_map = self._parse_categories(categories)
        
        for img_path in image_files:
            summary_data["total"] += 1
            
            try:
                # Load image
                img_pil = Image.open(img_path).convert('RGB')
                img_np = np.array(img_pil, dtype=np.float32) / 255.0
                img_tensor = torch.from_numpy(img_np)[None,]  # Add batch dimension
                
                # Calculate rating
                score = self._calculate_rating(img_pil, rating_method)
                score = max(1.0, min(10.0, score))
                
                summary_data["rated"] += 1
                
                # Determine category
                category = self._get_category(score, category_map)
                summary_data[category] += 1
                
                # Skip if below minimum score
                if score < min_score:
                    print(f"[BatchImageRater] Skipping {os.path.basename(img_path)} (score {score:.1f} < {min_score})")
                    continue
                
                # Organize if enabled
                if organize_by_score and copy_mode != "keep_original":
                    new_path = self._organize_image(
                        img_pil, img_path, score, category,
                        output_base, copy_mode, filename_with_score
                    )
                    paths.append(new_path)
                else:
                    paths.append(img_path)
                
                # Add to results
                rated_images.append(img_tensor)
                scores.append(score)
                
                print(f"[BatchImageRater] ✓ {os.path.basename(img_path)}: {score:.1f}/10 ({category})")
                
            except Exception as e:
                summary_data["errors"] += 1
                print(f"[BatchImageRater] ✗ Error processing {img_path}: {e}")
        
        # Convert to tensors
        if rated_images:
            images_tensor = torch.cat(rated_images, dim=0)
            scores_tensor = torch.tensor(scores, dtype=torch.float32)
            paths_str = "\n".join(paths)
        else:
            images_tensor = torch.zeros(1)
            scores_tensor = torch.zeros(1)
            paths_str = "No images met criteria"
        
        # Create summary
        summary = (
            f"📊 Batch Rating Summary\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Total images: {summary_data['total']}\n"
            f"Rated: {summary_data['rated']}\n"
            f"Errors: {summary_data['errors']}\n"
            f"\n"
            f"⭐ Excellent (8-10): {summary_data['excellent']}\n"
            f"👍 Good (5-7): {summary_data['good']}\n"
            f"✓ Acceptable (3-4): {summary_data['acceptable']}\n"
            f"✗ Rejected (1-2): {summary_data['rejected']}\n"
            f"\n"
            f"Average Score: {np.mean(scores):.2f}/10.0" if scores else "N/A"
        )
        
        print(f"\n[BatchImageRater] {summary}")
        
        return (images_tensor, scores_tensor, paths_str, summary)
    
    def _calculate_rating(self, img_pil, method="heuristic"):
        """Calculate rating using specified method."""
        import cv2
        img_np = np.array(img_pil)
        
        if method == "heuristic":
            return self._heuristic_rating(img_np)
        elif method == "blur_detection":
            return self._blur_rating(img_np)
        elif method == "contrast":
            return self._contrast_rating(img_np)
        elif method == "combined":
            sharpness = self._blur_rating(img_np)
            contrast = self._contrast_rating(img_np)
            heuristic = self._heuristic_rating(img_np)
            return (sharpness + contrast + heuristic) / 3.0
        else:
            return 5.0
    
    def _heuristic_rating(self, img_np):
        """Combined heuristic rating."""
        import cv2
        
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        
        # Sharpness
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        sharpness_score = min(10.0, sharpness / 50.0)
        
        # Contrast
        contrast = np.std(gray)
        contrast_score = min(10.0, contrast / 30.0)
        
        # Noise
        noise_score = 10.0 - min(5.0, sharpness / 100.0)
        
        return sharpness_score * 0.4 + contrast_score * 0.4 + noise_score * 0.2
    
    def _blur_rating(self, img_np):
        """Blur detection rating."""
        import cv2
        
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        return min(10.0, max(1.0, variance / 50.0))
    
    def _contrast_rating(self, img_np):
        """Contrast rating."""
        import cv2
        
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        
        histogram = cv2.calcHist([gray], [0], None, [256], [0, 256])
        non_zero_bins = np.count_nonzero(histogram)
        contrast_ratio = non_zero_bins / 256.0
        return max(1.0, min(10.0, contrast_ratio * 10.0))
    
    def _parse_categories(self, categories_str):
        """Parse category definitions."""
        category_map = {}
        
        for line in categories_str.strip().split('\n'):
            if ':' not in line:
                continue
            name, range_str = line.split(':', 1)
            name = name.strip()
            try:
                parts = range_str.replace('-', ':').split(':')
                min_score, max_score = float(parts[0]), float(parts[1])
                category_map[name] = (min_score, max_score)
            except (ValueError, IndexError):
                pass
        
        if not category_map:
            category_map = {
                "excellent": (8.0, 10.0),
                "good": (5.0, 7.9),
                "acceptable": (3.0, 4.9),
                "rejected": (1.0, 2.9)
            }
        
        return category_map
    
    def _get_category(self, score, category_map):
        """Get category for score."""
        for name, (min_score, max_score) in category_map.items():
            if min_score <= score <= max_score:
                return name
        return "rejected"
    
    def _organize_image(self, img_pil, original_path, score, category, 
                       output_base, copy_mode, filename_with_score):
        """Organize image into category folder."""
        import shutil
        
        # Create category directory
        category_dir = os.path.join(output_base, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Generate filename
        basename = os.path.basename(original_path)
        name, ext = os.path.splitext(basename)
        
        if filename_with_score:
            filename = f"{name}_score{score:.1f}{ext}"
        else:
            filename = basename
        
        new_path = os.path.join(category_dir, filename)
        
        # Copy or move
        if copy_mode == "copy":
            shutil.copy2(original_path, new_path)
        elif copy_mode == "move":
            shutil.move(original_path, new_path)
        
        return new_path


# Register node
NODE_CLASS_MAPPINGS = {
    "BatchImageRater": BatchImageRaterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchImageRater": "Batch Image Rater (Asset Page)"
}
