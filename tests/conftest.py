import pytest
from PIL import Image
import io

@pytest.fixture
def sample_image():
    """
    Creates a simple 10x10 red square image in memory for testing purposes.
    Returns a PIL Image object.
    """
    image = Image.new('RGB', (10, 10), color='red')
    return image
