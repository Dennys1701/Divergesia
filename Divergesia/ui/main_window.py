from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QListWidget, QListWidgetItem, QSplitter, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPixmap, QImage

from data.models import Paleta
import data.project_io as pio
from async_tasks.workers import ClusteringWorker, ExportWorker
from logic.harmony import (
    generar_complementarios, generar_analogos,
    generar_triadas, generar_tetradicos, generar_monocromatica
)
from logic.mockup import crear_mockup_ui
from ui.widgets import HSVAdjustWidget, PaletteHSVAdjustWidget

from PIL import Image
from PIL.ImageQt import ImageQt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Divergesia - Gestor de Paletas")
        self.resize(1200, 700)

        # Estado
        self.paleta_actual: Paleta | None = None
        self.paleta_original_colors: list | None = None  # Colores extraídos o cargados originalmente
        self.clustering_token = None
        self.workers = []
        self.loaded_image = None  # PIL Image cargada

        self._create_menu()
        self.status = self.statusBar()

        central = QWidget()
        central_layout = QVBoxLayout()
        central.setLayout(central_layout)
        self.setCentralWidget(central)

        splitter = QSplitter(Qt.Horizontal)
        central_layout.addWidget(splitter)

        # Panel izquierdo: carga de imagen, abrir paleta guardada y lista de paletas
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        btn_cargar = QPushButton("Cargar imagen...")
        btn_cargar.clicked.connect(self.on_cargar_imagen)
        left_layout.addWidget(btn_cargar)
        btn_abrir = QPushButton("Abrir paleta...")
        btn_abrir.clicked.connect(self.on_abrir_paleta)
        left_layout.addWidget(btn_abrir)
        self.lista_paletas = QListWidget()
        self.lista_paletas.itemClicked.connect(self._on_paleta_seleccionada)
        left_layout.addWidget(QLabel("Paletas en sesión:"))
        left_layout.addWidget(self.lista_paletas, 1)
        splitter.addWidget(left_widget)

        # Panel central: mostrar imagen original, swatches y mockup
        center_widget = QWidget()
        center_layout = QVBoxLayout()
        center_widget.setLayout(center_layout)

        # Label para imagen original en un ScrollArea
        center_layout.addWidget(QLabel("Imagen cargada:"))
        self.scroll_original = QScrollArea()
        self.scroll_original.setWidgetResizable(True)
        self.label_original = QLabel()
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setScaledContents(True)
        self.scroll_original.setWidget(self.label_original)
        self.label_original.setMaximumSize(300, 300)
        center_layout.addWidget(self.scroll_original, 2)

        # Contenedor de swatches de colores
        center_layout.addWidget(QLabel("Colores de la paleta:"))
        colors_container = QWidget()
        self.colors_layout = QHBoxLayout()
        colors_container.setLayout(self.colors_layout)
        center_layout.addWidget(colors_container, 0)

        # Vista de mockup
        center_layout.addWidget(QLabel("Mockup de paleta:"))
        self.label_mockup = QLabel()
        self.label_mockup.setAlignment(Qt.AlignCenter)
        self.label_mockup.setScaledContents(True)
        self.label_mockup.setMaximumSize(200, 200)
        center_layout.addWidget(self.label_mockup, 1)

        splitter.addWidget(center_widget)

        # Panel derecho: ajustes y acciones
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        # Widget para ajustes HSV
        self.palette_adjust_widget = PaletteHSVAdjustWidget()
        self.palette_adjust_widget.palette_changed.connect(self.on_palette_adjusted)
        right_layout.addWidget(self.palette_adjust_widget)
        # Botón para revertir a paleta original
        self.btn_revertir = QPushButton("Revertir a paleta original")
        self.btn_revertir.clicked.connect(self.on_revertir_paleta)
        self.btn_revertir.setEnabled(False)
        right_layout.addWidget(self.btn_revertir)
        # Botón guardar
        btn_guardar = QPushButton("Guardar paleta...")
        btn_guardar.clicked.connect(self.on_guardar_paleta)
        right_layout.addWidget(btn_guardar)
        # Generar armonía
        armonia_label = QLabel("Generar armonía:")
        right_layout.addWidget(armonia_label)
        btn_comp = QPushButton("Complementarios")
        btn_comp.clicked.connect(lambda: self.on_generar_armonia('complementario'))
        right_layout.addWidget(btn_comp)
        btn_analog = QPushButton("Análogos")
        btn_analog.clicked.connect(lambda: self.on_generar_armonia('analogos'))
        right_layout.addWidget(btn_analog)
        btn_triadas = QPushButton("Triadas")
        btn_triadas.clicked.connect(lambda: self.on_generar_armonia('triadas'))
        right_layout.addWidget(btn_triadas)
        btn_tetr = QPushButton("Tétradas")
        btn_tetr.clicked.connect(lambda: self.on_generar_armonia('tetradicos'))
        right_layout.addWidget(btn_tetr)
        btn_mono = QPushButton("Monocromática")
        btn_mono.clicked.connect(lambda: self.on_generar_armonia('monocromatica'))
        right_layout.addWidget(btn_mono)
        right_layout.addStretch()
        splitter.addWidget(right_widget)

    def _create_menu(self):
        menubar = self.menuBar()
        menu_archivo = menubar.addMenu("Archivo")
        action_cargar = QAction("Cargar imagen...", self)
        action_cargar.triggered.connect(self.on_cargar_imagen)
        menu_archivo.addAction(action_cargar)
        action_abrir = QAction("Abrir paleta...", self)
        action_abrir.triggered.connect(self.on_abrir_paleta)
        menu_archivo.addAction(action_abrir)
        action_guardar = QAction("Guardar paleta...", self)
        action_guardar.triggered.connect(self.on_guardar_paleta)
        menu_archivo.addAction(action_guardar)
        menu_archivo.addSeparator()
        action_exit = QAction("Salir", self)
        action_exit.triggered.connect(self.close)
        menu_archivo.addAction(action_exit)

    def on_cargar_imagen(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        try:
            img = Image.open(path)
            self.loaded_image = img
            # Mostrar versión escalada
            qt_img = ImageQt(img.convert('RGBA'))
            pix = QPixmap.fromImage(QImage(qt_img))
            pix = pix.scaled(self.label_original.maximumSize(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_original.setPixmap(pix)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la imagen: {e}")
            return
        # Extraer colores
        worker = ClusteringWorker(path, n_colors=5)
        worker.resultado.connect(self.handle_colores_extraidos)
        worker.error.connect(lambda msg: QMessageBox.critical(self, "Error", msg))
        worker.start()
        self.workers.append(worker)
        self.clustering_token = f"{path}:5"
        self.status.showMessage("Extrayendo colores...", 2000)

    def on_abrir_paleta(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir paleta JSON", "", "JSON (*.json)")
        if not path:
            return
        try:
            paleta = pio.cargar_paleta_desde_archivo(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la paleta: {e}")
            return
        colores = paleta.colores
        # Guardar como paleta original para revertir
        self.paleta_original_colors = colores.copy()
        self.btn_revertir.setEnabled(True)
        # Mostrar en lista
        nombre = paleta.nombre or "Paleta cargada"
        paleta.origen_imagen_path = path
        self.paleta_actual = paleta
        item = QListWidgetItem(nombre)
        item.setData(Qt.UserRole, paleta)
        self.lista_paletas.addItem(item)
        self.lista_paletas.setCurrentItem(item)
        # Mostrar swatches y mockup
        self._update_color_swatches(colores)
        self.palette_adjust_widget.set_palette(colores)
        self._update_mockup(colores)
        # No cambia imagen original mostrada
        self.status.showMessage(f"Paleta cargada desde {path}", 3000)

    def handle_colores_extraidos(self, colores: list, token: str):
        if token != self.clustering_token:
            return
        # Guardar colores originales para revertir
        self.paleta_original_colors = colores.copy()
        self.btn_revertir.setEnabled(True)
        nombre = "Paleta desde imagen"
        paleta = Paleta(nombre=nombre, colores=colores, origen_imagen_path=token.split(':')[0])
        self.paleta_actual = paleta
        current_item = self.lista_paletas.currentItem()
        if current_item:
            current_item.setText(nombre)
            current_item.setData(Qt.UserRole, paleta)
        else:
            item = QListWidgetItem(nombre)
            item.setData(Qt.UserRole, paleta)
            self.lista_paletas.addItem(item)
            self.lista_paletas.setCurrentItem(item)
        self._update_color_swatches(colores)
        self.palette_adjust_widget.set_palette(colores)
        self._update_mockup(colores)
        self.status.showMessage("Colores extraídos", 3000)

    def on_revertir_paleta(self):
        """Revertir a la paleta original extraída o cargada."""
        if not self.paleta_original_colors:
            return
        originales = self.paleta_original_colors.copy()
        nombre = self.paleta_actual.nombre if self.paleta_actual else "Paleta"
        paleta = Paleta(nombre=nombre, colores=originales,
                        origen_imagen_path=self.paleta_actual.origen_imagen_path if self.paleta_actual else "")
        self.paleta_actual = paleta
        # Actualizar lista: texto y datos
        current_item = self.lista_paletas.currentItem()
        if current_item:
            current_item.setText(nombre)
            current_item.setData(Qt.UserRole, paleta)
        self._update_color_swatches(originales)
        self.palette_adjust_widget.set_palette(originales)
        self._update_mockup(originales)
        self.status.showMessage("Paleta revertida a original", 3000)

    def _update_color_swatches(self, colores: list):
        for i in reversed(range(self.colors_layout.count())):
            widget = self.colors_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for color in colores:
            lbl = QLabel()
            lbl.setFixedSize(40, 40)
            r, g, b = color
            lbl.setStyleSheet(f"background-color: rgb({r},{g},{b}); border: 1px solid #000;")
            self.colors_layout.addWidget(lbl)

    def _update_mockup(self, colores: list):
        try:
            img = crear_mockup_ui(colores, size=(200, 200))
            qim = ImageQt(img.convert('RGBA'))
            pix = QPixmap.fromImage(QImage(qim))
            pix = pix.scaled(self.label_mockup.maximumSize(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_mockup.setPixmap(pix)
        except Exception as e:
            print(f"Error generando mockup: {e}")

    def on_palette_adjusted(self, nuevos_colores: list):
        if not self.paleta_actual:
            return
        self.paleta_actual.colores = nuevos_colores
        self._update_color_swatches(nuevos_colores)
        self._update_mockup(nuevos_colores)
        self.status.showMessage("Paleta ajustada", 1000)

    def on_guardar_paleta(self):
        if not self.paleta_actual:
            QMessageBox.information(self, "Info", "No hay paleta para guardar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Guardar paleta", "", "JSON (*.json);;CSS (*.css);;CSV (*.csv)")
        if not path:
            return
        ext = path.split('.')[-1].lower()
        formato = ext if ext in ('json', 'css', 'csv') else 'json'
        worker = ExportWorker(self.paleta_actual, path, formato=formato)
        worker.finished.connect(lambda p: self.status.showMessage(f"Guardado en {p}", 3000))
        worker.error.connect(lambda msg: QMessageBox.critical(self, "Error", msg))
        worker.start()
        self.workers.append(worker)

    def on_generar_armonia(self, tipo: str):
        if not self.paleta_actual:
            QMessageBox.information(self, "Info", "No hay paleta actual para generar armonía.")
            return
        base_colors = self.paleta_actual.colores
        try:
            if tipo == 'complementario':
                nuevos = generar_complementarios(base_colors)
                nombre = f"{self.paleta_actual.nombre} - Complementarios"
            elif tipo == 'analogos':
                nuevos = generar_analogos(base_colors)
                nombre = f"{self.paleta_actual.nombre} - Análogos"
            elif tipo == 'triadas':
                nuevos = generar_triadas(base_colors)
                nombre = f"{self.paleta_actual.nombre} - Triadas"
            elif tipo == 'tetradicos':
                nuevos = generar_tetradicos(base_colors)
                nombre = f"{self.paleta_actual.nombre} - Tétradicos"
            elif tipo == 'monocromatica':
                nuevos = generar_monocromatica(base_colors)
                nombre = f"{self.paleta_actual.nombre} - Monocromática"
            else:
                return
            paleta = Paleta(nombre=nombre, colores=nuevos, origen_imagen_path=self.paleta_actual.origen_imagen_path, armonia_tipo=tipo)
            self.paleta_actual = paleta
            current_item = self.lista_paletas.currentItem()
            if current_item:
                current_item.setText(nombre)
                current_item.setData(Qt.UserRole, paleta)
            self._update_color_swatches(nuevos)
            self.palette_adjust_widget.set_palette(nuevos)
            self._update_mockup(nuevos)
            self.status.showMessage(f"Armonía {tipo} generada", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generando armonía: {e}")

    def _on_paleta_seleccionada(self, item: QListWidgetItem):
        paleta = item.data(Qt.UserRole)
        if not isinstance(paleta, Paleta):
            return
        self.paleta_actual = paleta
        colores = paleta.colores
        self._update_color_swatches(colores)
        self.palette_adjust_widget.set_palette(colores)
        self._update_mockup(colores)
        self.status.showMessage(f"Paleta '{paleta.nombre}' seleccionada", 2000)

    def closeEvent(self, event):
        for w in self.workers:
            try:
                if hasattr(w, 'terminate'):
                    w.terminate()
            except Exception:
                pass
        event.accept()
