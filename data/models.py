from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from logic.color_utils import adjust_palette_hsv

@dataclass
class Paleta:
    """Representa una paleta de colores con metadata y funciones de ajuste."""
    nombre: str
    colores: List[Tuple[int, int, int]]
    origen_imagen_path: str = ""
    armonia_tipo: str = ""
    parametros: Dict = field(default_factory=dict)
    archivo_guardado: Optional[str] = None

    def to_dict(self) -> Dict:
        """Serializa la paleta a un diccionario JSON-serializable."""
        return {
            'nombre': self.nombre,
            'colores': [list(c) for c in self.colores],  # convertir tuplas a listas para JSON
            'origen_imagen_path': self.origen_imagen_path,
            'armonia_tipo': self.armonia_tipo,
            'parametros': self.parametros,
            'archivo_guardado': self.archivo_guardado,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Paleta':
        """Crea una instancia de Paleta a partir de un diccionario (p. ej. cargado de JSON)."""
        nombre = data.get('nombre', '')
        colores_raw = data.get('colores', [])
        # Convertir listas internas a tuplas
        colores = [tuple(c) for c in colores_raw]
        origen = data.get('origen_imagen_path', '')
        armonia = data.get('armonia_tipo', '')
        parametros = data.get('parametros', {}) or {}
        archivo = data.get('archivo_guardado')
        paleta = cls(
            nombre=nombre,
            colores=colores,
            origen_imagen_path=origen,
            armonia_tipo=armonia,
            parametros=parametros,
            archivo_guardado=archivo,
        )
        return paleta

    def apply_hsv_shift(self, hue_shift_deg: float = 0.0, sat_offset_pct: float = 0.0, val_offset_pct: float = 0.0) -> None:
       
        if not self.colores:
            return
        nuevos = adjust_palette_hsv(self.colores, hue_shift_deg, sat_offset_pct, val_offset_pct)
        self.colores = nuevos
        # Registrar en parámetros
        self.parametros['hsv_shift'] = {
            'hue_shift_deg': hue_shift_deg,
            'sat_offset_pct': sat_offset_pct,
            'val_offset_pct': val_offset_pct,
        }

    def with_hsv_shift(self, hue_shift_deg: float = 0.0, sat_offset_pct: float = 0.0, val_offset_pct: float = 0.0) -> 'Paleta':
       
        nuevos = adjust_palette_hsv(self.colores, hue_shift_deg, sat_offset_pct, val_offset_pct)
        nuevos_parametros = dict(self.parametros)
        nuevos_parametros['hsv_shift'] = {
            'hue_shift_deg': hue_shift_deg,
            'sat_offset_pct': sat_offset_pct,
            'val_offset_pct': val_offset_pct,
        }
        nueva = Paleta(
            nombre=f"{self.nombre} (HSV shift)",
            colores=nuevos,
            origen_imagen_path=self.origen_imagen_path,
            armonia_tipo=self.armonia_tipo,
            parametros=nuevos_parametros,
            archivo_guardado=None,
        )
        return nueva

    def __post_init__(self):
        # Validaciones básicas de colores
        validated = []
        for c in self.colores:
            if (not isinstance(c, tuple)) or len(c) != 3:
                raise ValueError(f"Color inválido en Paleta: {c}")
            r, g, b = c
            if not all(isinstance(ch, int) and 0 <= ch <= 255 for ch in (r, g, b)):
                raise ValueError(f"Valores de color deben ser ints en 0-255: {c}")
            validated.append((r, g, b))
        self.colores = validated
        # Inicializar parámetros si no existe
        if self.parametros is None:
            self.parametros = {}