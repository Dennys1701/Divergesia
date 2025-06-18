

from PySide6.QtCore import QThread, Signal
from PIL import Image
from data.models import Paleta
import data.project_io as pio
import traceback
from logic.clustering import extraer_colores_dominantes


class ClusteringWorker(QThread):
   
    # Emite la lista de colores (tuplas RGB) y un token identificador para validar resultados asincrónicos
    resultado = Signal(list, str)
    error = Signal(str)

    def __init__(self, image_path: str, n_colors: int = 5):
        super().__init__()
        self.image_path = image_path
        self.n_colors = n_colors

    def run(self):
        try:
            # Abrir imagen con PIL
            img = Image.open(self.image_path)
            # Extraer colores dominantes usando la lógica definida
            colores = extraer_colores_dominantes(img, n_colors=self.n_colors)
            # Generar token: combina ruta y número de colores para evitar resultados desfasados
            token = f"{self.image_path}:{self.n_colors}"
            # Emitir resultado
            self.resultado.emit(colores, token)
        except Exception as e:
            # Log de excepción para depuración
            traceback.print_exc()
            # Emitir señal de error con mensaje
            self.error.emit(f"Error en clustering: {e}")


class ExportWorker(QThread):
   
    # Emite la ruta de salida en caso de éxito
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, paleta: Paleta, path: str, formato: str = 'json'):
        super().__init__()
        self.paleta = paleta
        self.path = path
        self.formato = formato.lower()

    def run(self):
        try:
            if self.formato == 'json':
                # Exportar JSON usando project_io
                pio.guardar_paleta_a_archivo(self.paleta, self.path)
            elif self.formato == 'css':
                self._exportar_css()
            elif self.formato == 'csv':
                self._exportar_csv()
            else:
                raise ValueError(f"Formato de exportación no soportado: {self.formato}")
            # Emitir señal de finalización con la ruta de archivo exportado
            self.finished.emit(self.path)
        except Exception as e:
            traceback.print_exc()
            self.error.emit(f"Error exportando paleta: {e}")

    def _exportar_csv(self):
        import csv
        try:
            with open(self.path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Cabecera CSV
                writer.writerow(['R', 'G', 'B', 'Hex'])
                for color in self.paleta.colores:
                    hexc = '#{:02X}{:02X}{:02X}'.format(*color)
                    writer.writerow([color[0], color[1], color[2], hexc])
        except Exception:
            # Propagar excepción para que sea capturada en run()
            raise

    def _exportar_css(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                # Comentario con nombre de la paleta
                f.write(f"/* Paleta: {self.paleta.nombre} */\n")
                f.write(":root {\n")
                for idx, color in enumerate(self.paleta.colores):
                    hexc = '#{:02X}{:02X}{:02X}'.format(*color)
                    # Definir variable CSS --color-1, --color-2, etc.
                    f.write(f"  --color-{idx+1}: {hexc};\n")
                f.write("}\n")
        except Exception:
            raise
