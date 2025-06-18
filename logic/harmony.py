from typing import List, Tuple
from logic.color_utils import rgb_to_hsv_tuple, hsv_to_rgb_tuple


def generar_complementarios(base_colors: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
   
    resultados = []
    for color in base_colors:
        h, s, v = rgb_to_hsv_tuple(color)
        h2 = (h + 0.5) % 1.0
        rgb2 = hsv_to_rgb_tuple((h2, s, v))
        resultados.append(rgb2)
    return resultados


def generar_analogos(base_colors: List[Tuple[int, int, int]], angle_deg: float = 30.0) -> List[Tuple[int, int, int]]:
    
    resultados = []
    shift = angle_deg / 360.0
    for color in base_colors:
        h, s, v = rgb_to_hsv_tuple(color)
        h2 = (h + shift) % 1.0
        rgb2 = hsv_to_rgb_tuple((h2, s, v))
        resultados.append(rgb2)
    return resultados


def generar_triadas(base_colors: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    
    resultados = []
    shift = 1/3  # 120° en fracción de 1
    for color in base_colors:
        h, s, v = rgb_to_hsv_tuple(color)
        h2 = (h + shift) % 1.0
        rgb2 = hsv_to_rgb_tuple((h2, s, v))
        resultados.append(rgb2)
    return resultados


def generar_tetradicos(base_colors: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    
    resultados = []
    shift = 0.25  # 90°
    for color in base_colors:
        h, s, v = rgb_to_hsv_tuple(color)
        h2 = (h + shift) % 1.0
        rgb2 = hsv_to_rgb_tuple((h2, s, v))
        resultados.append(rgb2)
    return resultados


def generar_monocromatica(base_colors: List[Tuple[int, int, int]], adjust_pct: float = 20.0) -> List[Tuple[int, int, int]]:
   
    resultados = []
    for color in base_colors:
        h, s, v = rgb_to_hsv_tuple(color)
        delta = adjust_pct / 100.0
        if v > 0.5:
            v2 = max(0.0, v - delta)
        else:
            v2 = min(1.0, v + delta)
        rgb2 = hsv_to_rgb_tuple((h, s, v2))
        resultados.append(rgb2)
    return resultados
