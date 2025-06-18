
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from typing import List, Tuple


def extraer_colores_dominantes(
    img: Image.Image,
    n_colors: int = 5,
    resize_for_speed: bool = True,
    max_size: int = 200
) -> List[Tuple[int, int, int]]:
   
    # Convertir a RGB
    img_rgb = img.convert('RGB')
    # Redimensionar para velocidad si procede
    if resize_for_speed:
        w, h = img_rgb.size
        max_dim = max(w, h)
        if max_dim > max_size:
            scale = max_size / max_dim
            new_w = int(w * scale)
            new_h = int(h * scale)
            # Seleccionar filtro de resampling: Pillow>=9 usa Image.Resampling.LANCZOS
            try:
                resample_filter = Image.Resampling.LANCZOS
            except AttributeError:
                # Pillow<9
                resample_filter = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
            img_rgb = img_rgb.resize((new_w, new_h), resample_filter)
    # Obtener datos de píxeles
    arr = np.array(img_rgb)  # shape (H, W, 3)
    pixels = arr.reshape(-1, 3).astype(float)
    # Si hay menos píxeles que n_colors, retornar los únicos
    if pixels.shape[0] < n_colors:
        unique = np.unique(pixels, axis=0)
        colores = [tuple(map(int, u)) for u in unique]
        return colores
    # KMeans
    num_pixels = pixels.shape[0]
    if num_pixels > 10000:
        idx = np.random.choice(num_pixels, 10000, replace=False)
        sample = pixels[idx]
    else:
        sample = pixels
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(sample)
    centers = kmeans.cluster_centers_
    colores = []
    for center in centers:
        r, g, b = center
        r = int(round(r)); g = int(round(g)); b = int(round(b))
        r = max(0, min(r, 255)); g = max(0, min(g, 255)); b = max(0, min(b, 255))
        colores.append((r, g, b))
    return colores
