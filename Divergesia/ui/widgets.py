from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout, QGroupBox
from PySide6.QtCore import Qt, Signal
from logic.color_utils import rgb_to_hsv_tuple, hsv_to_rgb_tuple


class HSVAdjustWidget(QWidget):
  
    valor_cambiado = Signal(float, float, float)  # h, s, v en [0,1]

    def __init__(self):
        super().__init__()

        # Crear sliders
        self.slider_h = QSlider(Qt.Horizontal)
        self.slider_h.setRange(0, 360)
        self.slider_h.setSingleStep(1)

        self.slider_s = QSlider(Qt.Horizontal)
        self.slider_s.setRange(0, 100)
        self.slider_s.setSingleStep(1)

        self.slider_v = QSlider(Qt.Horizontal)
        self.slider_v.setRange(0, 100)
        self.slider_v.setSingleStep(1)

        # Crear labels
        self.label_h = QLabel("Matiz (H): 0°")
        self.label_s = QLabel("Saturación (S): 0%")
        self.label_v = QLabel("Valor (V): 0%")

        # Botón de reset
        self.reset_button = QPushButton("Reset")

        # Layout principal
        main_layout = QVBoxLayout()

        # Fila de Matiz
        row_h = QHBoxLayout()
        row_h.addWidget(self.label_h)
        row_h.addWidget(self.slider_h)
        main_layout.addLayout(row_h)

        # Fila de Saturación
        row_s = QHBoxLayout()
        row_s.addWidget(self.label_s)
        row_s.addWidget(self.slider_s)
        main_layout.addLayout(row_s)

        # Fila de Valor
        row_v = QHBoxLayout()
        row_v.addWidget(self.label_v)
        row_v.addWidget(self.slider_v)
        main_layout.addLayout(row_v)

        # Fila de Reset
        row_reset = QHBoxLayout()
        row_reset.addStretch()
        row_reset.addWidget(self.reset_button)
        main_layout.addLayout(row_reset)

        self.setLayout(main_layout)

        # Conectar señales de sliders a manejador
        self.slider_h.valueChanged.connect(self._on_slider_changed)
        self.slider_s.valueChanged.connect(self._on_slider_changed)
        self.slider_v.valueChanged.connect(self._on_slider_changed)

        # Conectar reset
        self.reset_button.clicked.connect(self.reset)

        # Inicializar valores a 0
        self.set_hsv(0.0, 0.0, 0.0)

    def _on_slider_changed(self, _value=None):
        """
        Actualiza labels según el valor de los sliders y emite valor_cambiado
        con valores normalizados.
        """
        h_deg = self.slider_h.value()
        s_pct = self.slider_s.value()
        v_pct = self.slider_v.value()

        # Actualizar textos
        self.label_h.setText(f"Matiz (H): {h_deg}°")
        self.label_s.setText(f"Saturación (S): {s_pct}%")
        self.label_v.setText(f"Valor (V): {v_pct}%")

        # Normalizar a [0,1]
        h_norm = h_deg / 360.0
        s_norm = s_pct / 100.0
        v_norm = v_pct / 100.0

        # Emitir señal con valores normalizados
        self.valor_cambiado.emit(h_norm, s_norm, v_norm)

    def set_hsv(self, h: float, s: float, v: float):
        """
        Establece los sliders y labels a los valores HSV dados (normalizados en [0,1]).
        Bloquea señales durante la actualización para no emitir valor_cambiado.
        """
        # Convertir a unidades de slider
        h_deg = int(round(h * 360))
        s_pct = int(round(s * 100))
        v_pct = int(round(v * 100))

        # Bloquear señales
        self.slider_h.blockSignals(True)
        self.slider_s.blockSignals(True)
        self.slider_v.blockSignals(True)

        # Ajustar sliders
        self.slider_h.setValue(h_deg)
        self.slider_s.setValue(s_pct)
        self.slider_v.setValue(v_pct)

        # Actualizar labels
        self.label_h.setText(f"Matiz (H): {h_deg}°")
        self.label_s.setText(f"Saturación (S): {s_pct}%")
        self.label_v.setText(f"Valor (V): {v_pct}%")

        # Desbloquear señales
        self.slider_h.blockSignals(False)
        self.slider_s.blockSignals(False)
        self.slider_v.blockSignals(False)

    def reset(self):
        
        self.set_hsv(0.0, 0.0, 0.0)


class PaletteHSVAdjustWidget(QWidget):
   
    palette_changed = Signal(list)  # Emite lista de tuplas (R,G,B)

    def __init__(self):
        super().__init__()
        # Sliders de ajustes
        # Hue shift: -180 a +180
        self.slider_hue_shift = QSlider(Qt.Horizontal)
        self.slider_hue_shift.setRange(-180, 180)
        self.slider_hue_shift.setSingleStep(1)

        # Saturation offset: -100 a +100
        self.slider_sat_offset = QSlider(Qt.Horizontal)
        self.slider_sat_offset.setRange(-100, 100)
        self.slider_sat_offset.setSingleStep(1)

        # Value offset: -100 a +100
        self.slider_val_offset = QSlider(Qt.Horizontal)
        self.slider_val_offset.setRange(-100, 100)
        self.slider_val_offset.setSingleStep(1)

        # Labels
        self.label_hue_shift = QLabel("Hue Shift: 0°")
        self.label_sat_offset = QLabel("Sat Offset: 0%")
        self.label_val_offset = QLabel("Val Offset: 0%")

        # Botón de reset ajustes
        self.reset_button = QPushButton("Reset ajustes")

        # Layout
        main_layout = QVBoxLayout()

        # Agrupar en un GroupBox
        group = QGroupBox("Ajustes HSV de paleta")
        group_layout = QVBoxLayout()

        # Hue shift row
        row_hue = QHBoxLayout()
        row_hue.addWidget(self.label_hue_shift)
        row_hue.addWidget(self.slider_hue_shift)
        group_layout.addLayout(row_hue)

        # Sat offset row
        row_sat = QHBoxLayout()
        row_sat.addWidget(self.label_sat_offset)
        row_sat.addWidget(self.slider_sat_offset)
        group_layout.addLayout(row_sat)

        # Val offset row
        row_val = QHBoxLayout()
        row_val.addWidget(self.label_val_offset)
        row_val.addWidget(self.slider_val_offset)
        group_layout.addLayout(row_val)

        # Reset row
        row_reset = QHBoxLayout()
        row_reset.addStretch()
        row_reset.addWidget(self.reset_button)
        group_layout.addLayout(row_reset)

        group.setLayout(group_layout)
        main_layout.addWidget(group)
        self.setLayout(main_layout)

        # Estado interno
        self.original_palette = []  # Lista de tuplas RGB originales

        # Conectar señales de sliders
        self.slider_hue_shift.valueChanged.connect(self._on_adjustment_changed)
        self.slider_sat_offset.valueChanged.connect(self._on_adjustment_changed)
        self.slider_val_offset.valueChanged.connect(self._on_adjustment_changed)
        self.reset_button.clicked.connect(self.reset_adjustments)

        # Inicializar a cero
        self.reset_adjustments()

    def set_palette(self, palette: list):
       
        # Validar formato: lista de tuplas de 3 ints
        self.original_palette = [tuple(color) for color in palette]
        # Resetear sliders
        self.block_signals_and_reset_sliders()
        # Emitir la paleta original inicialmente
        self.palette_changed.emit(self.original_palette.copy())

    def block_signals_and_reset_sliders(self):
        # Bloquear señales de sliders temporalmente
        self.slider_hue_shift.blockSignals(True)
        self.slider_sat_offset.blockSignals(True)
        self.slider_val_offset.blockSignals(True)

        # Poner en cero
        self.slider_hue_shift.setValue(0)
        self.slider_sat_offset.setValue(0)
        self.slider_val_offset.setValue(0)

        # Actualizar labels
        self.label_hue_shift.setText("Hue Shift: 0°")
        self.label_sat_offset.setText("Sat Offset: 0%")
        self.label_val_offset.setText("Val Offset: 0%")

        # Desbloquear señales
        self.slider_hue_shift.blockSignals(False)
        self.slider_sat_offset.blockSignals(False)
        self.slider_val_offset.blockSignals(False)

    def _on_adjustment_changed(self, _value=None):
        """Cuando cambia algún slider, recalcula la paleta ajustada y emite palette_changed."""
        # Leer valores de sliders
        hue_shift_deg = self.slider_hue_shift.value()  # -180 a 180
        sat_offset_pct = self.slider_sat_offset.value()  # -100 a 100
        val_offset_pct = self.slider_val_offset.value()  # -100 a 100

        # Actualizar labels
        self.label_hue_shift.setText(f"Hue Shift: {hue_shift_deg}°")
        self.label_sat_offset.setText(f"Sat Offset: {sat_offset_pct}%")
        self.label_val_offset.setText(f"Val Offset: {val_offset_pct}%")

        # Aplicar transformación a cada color de la paleta original
        adjusted = []
        for color in self.original_palette:
            # Convertir RGB a HSV normalizado
            h, s, v = rgb_to_hsv_tuple(color)
            # h está en [0,1]; convertir shift a fracción
            h_new = (h + hue_shift_deg / 360.0) % 1.0
            # Ajustar s y v: s, v en [0,1]
            s_new = min(max(s + sat_offset_pct / 100.0, 0.0), 1.0)
            v_new = min(max(v + val_offset_pct / 100.0, 0.0), 1.0)
            # Convertir de vuelta a RGB
            rgb_new = hsv_to_rgb_tuple((h_new, s_new, v_new))
            adjusted.append(rgb_new)

        # Emitir paleta ajustada
        self.palette_changed.emit(adjusted)

    def reset_adjustments(self):
        """Resetea sliders a cero y emite la paleta original."""
        if not self.original_palette:
            # Aún no se ha establecido paleta; solo resetear sliders
            self.block_signals_and_reset_sliders()
            return
        self.block_signals_and_reset_sliders()
        # Emitir la paleta original
        self.palette_changed.emit(self.original_palette.copy())
