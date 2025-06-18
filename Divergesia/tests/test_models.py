import pytest
from data.models import Paleta


def test_to_from_dict():
    nombre = "Test"
    colores = [(10, 20, 30), (100, 150, 200)]
    origen = "path/to/image.png"
    armonia = "complementario"
    parametros = {'key': 'value'}
    archivo = "output.json"
    paleta = Paleta(nombre=nombre, colores=colores, origen_imagen_path=origen, armonia_tipo=armonia, parametros=parametros, archivo_guardado=archivo)
    d = paleta.to_dict()
    # Verificar estructura del dict
    assert d['nombre'] == nombre
    assert isinstance(d['colores'], list)
    assert d['colores'] == [list(c) for c in colores]
    assert d['origen_imagen_path'] == origen
    assert d['armonia_tipo'] == armonia
    assert d['parametros'] == parametros
    assert d['archivo_guardado'] == archivo
    # Reconstruir
    p2 = Paleta.from_dict(d)
    assert p2.nombre == nombre
    assert p2.colores == colores
    assert p2.origen_imagen_path == origen
    assert p2.armonia_tipo == armonia
    assert p2.parametros == parametros
    assert p2.archivo_guardado == archivo

@pytest.mark.parametrize("shift_h, shift_s, shift_v", [
    (0, 0, 0),
    (180, 0, 0),
    (0, 50, 0),
    (0, 0, -50),
])
def test_apply_hsv_shift_inplace_and_with(shift_h, shift_s, shift_v):
    colores = [(255, 0, 0), (0, 255, 0)]
    pal = Paleta(nombre="Original", colores=colores.copy())
    # Aplicar in-place
    pal.apply_hsv_shift(hue_shift_deg=shift_h, sat_offset_pct=shift_s, val_offset_pct=shift_v)
    # Verificar que pal.colores haya cambiado según with_hsv_shift
    pal2 = Paleta(nombre="Original", colores=colores.copy())
    pal2_shifted = pal2.with_hsv_shift(hue_shift_deg=shift_h, sat_offset_pct=shift_s, val_offset_pct=shift_v)
    assert pal.colores == pal2_shifted.colores
    # Verificar que parámetros se registren
    assert 'hsv_shift' in pal.parametros
    registro = pal.parametros['hsv_shift']
    assert registro['hue_shift_deg'] == shift_h
    assert registro['sat_offset_pct'] == shift_s
    assert registro['val_offset_pct'] == shift_v


def test_post_init_validation():
    # Color inválido: lista en vez de tupla
    with pytest.raises(ValueError):
        Paleta(nombre="Err", colores=[ [10,20,30] ])
    # Color con valor fuera de rango
    with pytest.raises(ValueError):
        Paleta(nombre="Err", colores=[(300,0,0)])
    # Colores vacíos es permitido
    pal = Paleta(nombre="Empty", colores=[])
    assert pal.colores == []
