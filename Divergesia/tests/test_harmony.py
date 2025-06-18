from typing import List, Tuple

def generar_complementarios(hsv_colors: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
    """Genera la lista de colores complementarios para cada color HSV."""
    return [((h + 0.5) % 1.0, s, v) for (h, s, v) in hsv_colors]


def generar_analogos(hsv_colors: List[Tuple[float, float, float]], offset: float = 1/12) -> List[List[Tuple[float, float, float]]]:
    """Genera una lista de listas de colores análogos para cada color HSV, desplazados por el offset."""
    resultado = []
    for (h, s, v) in hsv_colors:
        resultado.append([
            ((h - offset) % 1.0, s, v),
            (h, s, v),
            ((h + offset) % 1.0, s, v)
        ])
    return resultado


def generar_triadas(hsv_colors: List[Tuple[float, float, float]]) -> List[List[Tuple[float, float, float]]]:
    """Genera triadas equiláteras de cada color HSV."""
    resultado = []
    for (h, s, v) in hsv_colors:
        resultado.append([
            (h % 1.0, s, v),
            ((h + 1/3) % 1.0, s, v),
            ((h + 2/3) % 1.0, s, v)
        ])
    return resultado


def generar_tetradicos(hsv_colors: List[Tuple[float, float, float]], offset1: float = 1/3, offset2: float = 0.5) -> List[List[Tuple[float, float, float]]]:
    """Genera combinaciones tetrádicas para cada color HSV usando dos offsets."""
    resultado = []
    for (h, s, v) in hsv_colors:
        resultado.append([
            (h % 1.0, s, v),
            ((h + offset1) % 1.0, s, v),
            ((h + offset2) % 1.0, s, v),
            ((h + offset1 + offset2) % 1.0, s, v)
        ])
    return resultado


def generar_monocromatica(hsv_colors: List[Tuple[float, float, float]], variaciones: List[float] = [0.5, 0.8, 1.0]) -> List[List[Tuple[float, float, float]]]:
    """Genera versiones monocromáticas alterando el valor (brightness) del color."""
    resultado = []
    for (h, s, v) in hsv_colors:
        grupo = []
        for factor in variaciones:
            nuevo_v = max(0.0, min(1.0, v * factor))
            grupo.append((h, s, nuevo_v))
        resultado.append(grupo)
    return resultado