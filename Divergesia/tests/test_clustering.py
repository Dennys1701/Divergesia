import pytest
from PIL import Image
import numpy as np
from logic.clustering import extraer_colores_dominantes

def create_test_image(colors, size=(100,100)):
    # colors: list de tuples RGB; divide la imagen en vertical en regiones iguales
    w,h = size
    img = Image.new('RGB', size)
    region_w = w // len(colors)
    for i, color in enumerate(colors):
        for x in range(i*region_w, (i+1)*region_w if i < len(colors)-1 else w):
            for y in range(h):
                img.putpixel((x,y), color)
    return img

def test_extraer_colores_two_colors():
    # Imagen dividida en dos colores
    img = create_test_image([(255,0,0),(0,255,0)], size=(100,100))
    colores = extraer_colores_dominantes(img, n_colors=2, resize_for_speed=False)
    # Debe contener rojo y verde (en cualquier orden)
    assert set(colores) == {(255,0,0),(0,255,0)}