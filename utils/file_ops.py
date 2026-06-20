"""
File operations for ComfyUI Image Rater.
"""

import os
import shutil
from PIL import Image
from typing import List, Tuple

def create_directory(path: str) -> bool:
    """
    Create directory if it doesn't exist.
    
    Args:
        path: Directory path to create
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"[FileOps] Error creating directory {path}: {e}")
        return False

def save_image_to_path(image, path: str, quality: int = 95) -> bool:
    """
    Save PIL Image or numpy array to file path.
    
    Args:
        image: PIL Image or numpy array
        path: Output file path
        quality: JPEG quality (1-100)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert numpy array to PIL if needed
        if not isinstance(image, Image.Image):
            import numpy as np
            if isinstance(image, np.ndarray):
                image = Image.fromarray(image)
            else:
                print(f"[FileOps] Unknown image type: {type(image)}")
                return False
        
        # Ensure parent directory exists
        parent_dir = os.path.dirname(path)
        if parent_dir:
            create_directory(parent_dir)
        
        # Save based on extension
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            image.save(path, 'JPEG', quality=quality)
        elif ext == '.png':
            image.save(path, 'PNG')
        elif ext == '.webp':
            image.save(path, 'WEBP', quality=quality)
        else:
            image.save(path)  # Default
        
        return True
    except Exception as e:
        print(f"[FileOps] Error saving image to {path}: {e}")
        return False

def get_image_files(directory: str, extensions: List[str] = None) -> List[str]:
    """
    Get list of image files in directory.
    
    Args:
        directory: Directory to scan
        extensions: List of extensions to include (default: common image formats)
        
    Returns:
        List of file paths
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
    
    image_files = []
    
    try:
        for filename in os.listdir(directory):
            ext = os.path.splitext(filename)[1].lower()
            if ext in extensions:
                image_files.append(os.path.join(directory, filename))
    except Exception as e:
        print(f"[FileOps] Error scanning directory {directory}: {e}")
    
    return sorted(image_files)

def move_file(src: str, dst: str, overwrite: bool = False) -> Tuple[bool, str]:
    """
    Move file from src to dst.
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        if not os.path.exists(src):
            return False, f"Source file not found: {src}"
        
        if os.path.exists(dst) and not overwrite:
            return False, f"Destination already exists: {dst}"
        
        # Ensure destination directory exists
        dst_dir = os.path.dirname(dst)
        if dst_dir:
            create_directory(dst_dir)
        
        shutil.move(src, dst)
        return True, f"Moved: {src} -> {dst}"
    except Exception as e:
        return False, f"Error moving file: {e}"

def copy_file(src: str, dst: str, overwrite: bool = False) -> Tuple[bool, str]:
    """
    Copy file from src to dst.
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        if not os.path.exists(src):
            return False, f"Source file not found: {src}"
        
        if os.path.exists(dst) and not overwrite:
            return False, f"Destination already exists: {dst}"
        
        # Ensure destination directory exists
        dst_dir = os.path.dirname(dst)
        if dst_dir:
            create_directory(dst_dir)
        
        shutil.copy2(src, dst)
        return True, f"Copied: {src} -> {dst}"
    except Exception as e:
        return False, f"Error copying file: {e}"

def calculate_image_metrics(image_path: str) -> dict:
    """
    Calculate various image quality metrics.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary of metrics
    """
    import numpy as np
    import cv2
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "Could not load image"}
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Sharpness (Laplacian variance)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        
        # Contrast (standard deviation)
        contrast = np.std(gray)
        
        # Brightness (mean)
        brightness = np.mean(gray)
        
        # Color richness (std dev of color channels)
        if len(img.shape) == 3:
            color_richness = np.mean([np.std(img[:,:,i]) for i in range(3)])
        else:
            color_richness = 0
        
        return {
            "sharpness": float(sharpness),
            "contrast": float(contrast),
            "brightness": float(brightness),
            "color_richness": float(color_richness),
            "width": img.shape[1],
            "height": img.shape[0]
        }
    except Exception as e:
        return {"error": str(e)}
