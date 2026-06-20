"""
Image Rater Node
Rates images using various quality metrics and/or ML models.
"""

import torch
import numpy as np
from PIL import Image
import os

class ImageRaterNode:
    """
    Rates images on a scale of 1-10 based on quality metrics.
    
    Currently uses heuristic methods:
    - Sharpness detection
    - Noise estimation
    - Color distribution
    - Contrast analysis
    
    Future: ML-based rating model
    """
    
    CATEGORY = "utils/rating"
    FUNCTION = "rate_images"
    RETURN_NAMES = ("rated_images", "rating_scores", "metadata")
    RETURN_TYPES = ("IMAGE", "FLOAT", "STRING")
    OUTPUT_NODE = False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "rating_method": (["heuristic", "blur_detection", "contrast"],),
                "min_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.1}),
            },
            "optional": {
                "rating_model": ("RATING_MODEL",),
                "batch_name": ("STRING", {"default": "batch"}),
            }
        }
    
    def rate_images(self, images, rating_method="heuristic", min_score=0.0, 
                    rating_model=None, batch_name="batch"):
        """
        Rate a batch of images.
        
        Args:
            images: Tensor of shape [B, H, W, C]
            rating_method: Method to use for rating
            min_score: Minimum score threshold
            rating_model: Optional custom model
            batch_name: Name for this batch
            
        Returns:
            Tuple of (images, scores, metadata)
        """
        import cv2
        
        scores = []
        metadata_list = []
        
        for i, img_tensor in enumerate(images):
            # Convert tensor to numpy array
            img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            
            # Calculate rating based on method
            if rating_method == "heuristic":
                score = self._heuristic_rating(img_np)
            elif rating_method == "blur_detection":
                score = self._blur_rating(img_np)
            elif rating_method == "contrast":
                score = self._contrast_rating(img_np)
            else:
                score = 5.0  # Default middle score
            
            # Normalize to 1-10 scale
            score = max(1.0, min(10.0, score))
            
            scores.append(score)
            metadata_list.append(f"Image {i}: {score:.2f}/10.0 ({rating_method})")
        
        # Convert to tensors for ComfyUI
        scores_tensor = torch.tensor(scores, dtype=torch.float32)
        metadata_str = "\n".join(metadata_list)
        
        print(f"[ImageRater] Rated {len(images)} images")
        print(f"[ImageRater] Scores: {scores}")
        print(f"[ImageRater] Average: {np.mean(scores):.2f}/10.0")
        
        return (images, scores_tensor, metadata_str)
    
    def _heuristic_rating(self, img_np):
        """
        Combined heuristic rating based on multiple factors.
        """
        import cv2
        
        # Convert to grayscale
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        
        # 1. Sharpness (Laplacian variance)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        sharpness_score = min(10.0, sharpness / 50.0)  # Normalize
        
        # 2. Contrast (standard deviation)
        contrast = np.std(gray)
        contrast_score = min(10.0, contrast / 30.0)  # Normalize
        
        # 3. Noise estimation (high frequency content)
        noise_score = 10.0 - min(5.0, sharpness / 100.0)  # Less noise = higher score
        
        # Weighted average
        final_score = (sharpness_score * 0.4 + contrast_score * 0.4 + noise_score * 0.2)
        
        return final_score
    
    def _blur_rating(self, img_np):
        """
        Rate based on blur detection.
        Higher score = less blur = better quality.
        """
        import cv2
        
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        
        # Laplacian variance for blur detection
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        
        # Map variance to 1-10 scale
        # Typical variance: 0-500 (blurry to sharp)
        score = min(10.0, max(1.0, variance / 50.0))
        
        return score
    
    def _contrast_rating(self, img_np):
        """
        Rate based on contrast and color distribution.
        """
        import cv2
        
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        
        # Calculate contrast ratio
        histogram = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        # Good contrast = histogram spans full range
        non_zero_bins = np.count_nonzero(histogram)
        contrast_ratio = non_zero_bins / 256.0
        
        score = contrast_ratio * 10.0
        return max(1.0, min(10.0, score))
