from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple


def crear_mockup_ui(palette: List[Tuple[int, int, int]], size: Tuple[int, int] = (200, 200)) -> Image.Image:
   
    # Validaciones básicas
    if not isinstance(palette, list):
        raise TypeError(f"palette debe ser una lista de tuplas RGB, got {type(palette)}")
    for c in palette:
        if (not isinstance(c, tuple)) or len(c) != 3:
            raise ValueError(f"Cada elemento de palette debe ser tupla de 3 ints, got {c}")
        if not all(isinstance(ch, int) and 0 <= ch <= 255 for ch in c):
            raise ValueError(f"Valores de color deben ser ints entre 0 y 255, got {c}")

    width, height = size
    if width <= 0 or height <= 0:
        raise ValueError(f"Tamaño inválido: {size}")

    # Crear imagen base con fondo neutro (blanco)
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    n = len(palette)
    if n == 0:
        # Si no hay colores, devolver fondo blanco o con texto indicando 'sin colores'
        try:
            # Intentar dibujar texto central (si hay fuente disponible)
            text = "No colors"
            # Fuente por defecto; ajuste del tamaño
            font = ImageFont.load_default()
            text_w, text_h = draw.textsize(text, font=font)
            draw.text(((width - text_w) / 2, (height - text_h) / 2), text, fill=(0, 0, 0), font=font)
        except Exception:
            pass
        return img

    # Dibujar bloques de color
    # Calcular ancho de bloque; si no cabe exacto, el último bloque llenará el resto
    block_width = width // n
    for idx, color in enumerate(palette):
        x0 = idx * block_width
        # Para el último bloque, asegurar cubrir hasta el final
        x1 = (idx + 1) * block_width if idx < n - 1 else width
        # Dibujar rectángulo completo en altura
        draw.rectangle([x0, 0, x1, height], fill=color)

    # Opcional: dibujar bordes entre bloques
    # Usar color neutro (negro) o semitransparente si se desea
    for idx in range(1, n):
        x = idx * block_width
        # Línea vertical fina
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0), width=1)

    return img
