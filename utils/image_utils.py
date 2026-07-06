import base64
import mimetypes
from pathlib import Path
from io import BytesIO
from PIL import Image

def encode_image_to_base64(image_path: str, max_size: int = 1024) -> str:
    """
    Resizes, compresses, and encodes an image file into a base64 string.
    Reduces API payload size and token consumption.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found at {image_path}")
        
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "image/jpeg"
        
    with Image.open(path) as img:
        # Convert to RGB if needed (e.g. for PNGs with alpha)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            mime_type = "image/jpeg" # force jpeg for size
            
        # Resize if larger than max_size
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
        # Compress and save to buffer
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
    return f"data:{mime_type};base64,{encoded_string}"
