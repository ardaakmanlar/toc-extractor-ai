from PIL import Image, ImageEnhance, ImageFilter
import os
from tkinter import filedialog

def preprocess_image(img: Image.Image, max_size=1024, contrast_factor=2.0) -> Image.Image:
    """
    Preprocess the given image by resizing, converting to grayscale, enhancing contrast, and sharpening.
    """
    img = img.copy()
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_factor)
    img = img.filter(ImageFilter.SHARPEN)
    return img

def save_preprocessed_image(img: Image.Image, original_filename: str, output_dir="preprocessed_images") -> str:
    """
    Save the preprocessed image to a file in the specified output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    original_name = os.path.basename(original_filename)
    name, ext = os.path.splitext(original_name)
    preprocessed_filename = os.path.join(output_dir, f"{name}_preprocessed{ext}")
    img.save(preprocessed_filename)
    return preprocessed_filename


def load_images():
    image_paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")]
    )

    if not image_paths:
        return []

    try:
        images = [Image.open(path) for path in image_paths]
        return images
    except Exception as e:
        print("Error loading images:", e)
        return []