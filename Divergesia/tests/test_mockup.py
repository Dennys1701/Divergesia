import pytest
from logic.mockup import crear_mockup_ui
from PIL import Image

def test_mockup_size_and_type():
    paleta = [(240,240,240), (200,200,200), (0,0,0), (100,100,100), (255,255,255)]
    img = crear_mockup_ui(paleta, size=(320,200))
    assert isinstance(img, Image.Image)
    assert img.size == (320,200)