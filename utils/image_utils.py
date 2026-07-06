import base64
import mimetypes
from pathlib import Path

def encode_image_to_base64(image_path: str) -> str:
    """Encodes an image file into a base64 string for OpenRouter payloads."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found at {image_path}")
        
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "image/jpeg"
        
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
    return f"data:{mime_type};base64,{encoded_string}"
