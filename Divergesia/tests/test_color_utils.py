import pytest
from logic.color_utils import (
    rgb_to_hsv_tuple,
    hsv_to_rgb_tuple,
    adjust_color_hsv,
    adjust_palette_hsv
)

@pytest.mark.parametrize("rgb", [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (128, 64, 32),
    (0, 0, 0),
    (255, 255, 255),
])
def test_rgb_hsv_roundtrip(rgb):
    """Test que convierte RGB -> HSV -> RGB y se obtiene el color original."""
    h, s, v = rgb_to_hsv_tuple(rgb)
    rgb2 = hsv_to_rgb_tuple((h, s, v))
    assert rgb2 == rgb

@pytest.mark.parametrize("color, shift, expected", [
    ((255, 0, 0), 180, (0, 255, 255)),     # rojo complementario
    ((0, 255, 0), 180, (255, 0, 255)),     # verde complementario
    ((0, 0, 255), 180, (255, 255, 0)),     # azul complementario
])
def test_adjust_color_hue_shift(color, shift, expected):
    """Test de desplazamiento de matiz para obtener color complementario."""
    result = adjust_color_hsv(color, hue_shift_deg=shift)
    assert result == expected

@pytest.mark.parametrize("color, sat_offset, expected", [
    ((128, 128, 128), 50, None),  # gris (s=0) subir saturación debería quedarse en gris (no cambia)
    ((200, 100, 50), -50, None),   # reduce saturación: aproximar a gris
])
def test_adjust_color_saturation_offset(color, sat_offset, expected):
    """Test de offset de saturación. En caso de gris, no cambia; en otros se reduce o aumenta."""
    # Se prueba que el valor de saturación cambie dentro de rango [0,1]
    h, s_orig, v = rgb_to_hsv_tuple(color)
    new = adjust_color_hsv(color, hue_shift_deg=0, sat_offset_pct=sat_offset)
    h2, s_new, v2 = rgb_to_hsv_tuple(new)
    assert pytest.approx(v, rel=1e-3) == v2  # valor permanece
    # Si s_orig==0, s_new seguirá 0
    if s_orig == 0:
        assert pytest.approx(0.0, abs=1e-6) == s_new
    else:
        # s_new es s_orig + offset, pero clamp a [0,1]
        expected_s = max(0.0, min(s_orig + sat_offset / 100.0, 1.0))
        assert pytest.approx(expected_s, rel=1e-3) == s_new

@pytest.mark.parametrize("palette, shift_h, shift_s, shift_v", [
    ([(255, 0, 0), (0, 255, 0), (0, 0, 255)], 90, 0, 0),  # shift matiz 90°
    ([(50, 100, 150), (200, 50, 100)], 0, 20, -20),         # shift sat+val
])
def test_adjust_palette_hsv(palette, shift_h, shift_s, shift_v):
    """Test de ajuste de paleta completa."""
    result = adjust_palette_hsv(palette, hue_shift_deg=shift_h, sat_offset_pct=shift_s, val_offset_pct=shift_v)
    assert isinstance(result, list)
    assert len(result) == len(palette)
    # Verificar que cada color individual coincide con adjust_color_hsv
    for orig, new in zip(palette, result):
        expected = adjust_color_hsv(orig, hue_shift_deg=shift_h, sat_offset_pct=shift_s, val_offset_pct=shift_v)
        assert new == expected
