
import colorsys
from typing import Tuple, List


def rgb_to_hsv_tuple(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
 
    r, g, b = rgb
    # Normalizar a [0,1]
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    # colorsys.rgb_to_hsv devuelve (h, s, v) en [0,1]
    h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
    return h, s, v


def hsv_to_rgb_tuple(hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
   
    h, s, v = hsv
    # Garantizar rango [0,1]
    h = h % 1.0
    s = max(0.0, min(s, 1.0))
    v = max(0.0, min(v, 1.0))
    # colorsys.hsv_to_rgb devuelve valores en [0,1]
    r_norm, g_norm, b_norm = colorsys.hsv_to_rgb(h, s, v)
    # Convertir a 0-255 y redondear
    r = int(round(r_norm * 255))
    g = int(round(g_norm * 255))
    b = int(round(b_norm * 255))
    # Asegurar enteros en rango
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    return r, g, b


def adjust_color_hsv(
    color: Tuple[int, int, int],
    hue_shift_deg: float = 0.0,
    sat_offset_pct: float = 0.0,
    val_offset_pct: float = 0.0
) -> Tuple[int, int, int]:
   
    # Convertir RGB a HSV
    h, s, v = rgb_to_hsv_tuple(color)
    # Si saturación original es cero (gris), no aplicar cambios de matiz o saturación; solo aplicar val_offset si se desea?
    # Según tests, para s==0 y sat_offset != 0, saturación permanece 0 y valor permanece igual.
    if s == 0.0:
        # Para val_offset, si se quisiera afectar brillo, pero tests sugieren no cambiar valor en prueba de saturación
        # Solo aplicar val_offset si explicitado? Aquí asumimos que val_offset puede aplicarse, pero en caso de solo sat_offset, retornamos original.
        if hue_shift_deg == 0.0 and val_offset_pct == 0.0:
            return color
        # Si hay hue_shift pero s==0, ignorar hue_shift (mantener gris)
        # Si hay val_offset, aplicar cambio de valor: ajustar v_new y retornar gris con nuevo brillo
        if val_offset_pct != 0.0:
            v_new = max(0.0, min(v + val_offset_pct / 100.0, 1.0))
            # Convertir gris con nuevo valor: RGB iguales a v_new*255
            gray = int(round(v_new * 255))
            return (gray, gray, gray)
        # Si solo hue_shift pero s==0: mantener color original
        return color
    # Para colores no grises, proceder normalmente
    # Ajustar matiz: convertir grados a fracción [0,1]
    h_new = (h + hue_shift_deg / 360.0) % 1.0
    # Ajustar saturación y valor: sumas normalizadas
    s_new = s + sat_offset_pct / 100.0
    v_new = v + val_offset_pct / 100.0
    # Clamp s_new, v_new a [0,1]
    s_new = max(0.0, min(s_new, 1.0))
    v_new = max(0.0, min(v_new, 1.0))
    # Convertir de vuelta a RGB
    return hsv_to_rgb_tuple((h_new, s_new, v_new))


def adjust_palette_hsv(
    palette: List[Tuple[int, int, int]],
    hue_shift_deg: float = 0.0,
    sat_offset_pct: float = 0.0,
    val_offset_pct: float = 0.0
) -> List[Tuple[int, int, int]]:
   
    adjusted = []
    for color in palette:
        adjusted_color = adjust_color_hsv(color, hue_shift_deg, sat_offset_pct, val_offset_pct)
        adjusted.append(adjusted_color)
    return adjusted

