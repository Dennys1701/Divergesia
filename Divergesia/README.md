Divergesia

Aplicación de escritorio para la extracción, ajuste y gestión de paletas de colores.
Permite extraer colores dominantes de imágenes, ajustar valores HSV, generar armonías y mockups, y guardar/cargar paletas en varios formatos.

Características

Extracción de colores dominantes: Analiza una imagen y obtiene una paleta con los colores principales mediante clustering (KMeans).

Visualización de imagen cargada: Muestra la imagen original escalada a un tamaño manejable.

Ajuste HSV de paleta: Desplazamiento de matiz, saturación y valor para afinar la paleta.

Generación de armonías: Complementarios, análogos, triadas, tétradas y monocromática manteniendo el mismo número de colores.

Mockup visual: Representación gráfica de bloques de color de la paleta, para previsualizar la combinación.

Guardar y cargar paletas:

Exportar a JSON: incluye metadatos (nombre, origen, tipo de armonía, parámetros de ajuste).

Exportar a CSS: variables --color-1, --color-2, etc., para integrar en proyectos web.

Exportar a CSV: lista de R,G,B y valor hexadecimal.

Importar JSON: recarga la paleta guardada con sus metadatos.

Reversión a paleta original: Botón para restaurar la paleta extraída o cargada originalmente.

Interfaz responsiva: Operaciones de extracción y guardado en segundo plano mediante QThread.

Tests unitarios: Cobertura para utilidades de color, modelo de Paleta, clustering, armonía y mockup.

Requisitos

Python 3.8 o superior

Dependencias listadas en requirements.txt:

PySide6

Pillow

numpy

scikit-learn

pytest

Opcionalmente, para tests de UI: pytest-qt, y configurar QT_QPA_PLATFORM=offscreen en CI o entornos sin display.

Estructura del proyecto

Divergesia/
├── async_tasks/
│ ├── **init**.py
│ ├── thread_manager.py
│ └── workers.py
├── data/
│ ├── **init**.py
│ ├── models.py
│ └── project_io.py
├── logic/
│ ├── **init**.py
│ ├── clustering.py
│ ├── color_utils.py
│ ├── harmony.py
│ └── mockup.py
├── ui/
│ ├── **init**.py
│ ├── main_window.py
│ ├── widgets.py
│ └── resources/ # (opcional) imágenes, estilos, etc.
├── tests/
│ ├── **init**.py
│ ├── conftest.py
│ ├── test_color_utils.py
│ ├── test_models.py
│ ├── test_clustering.py
│ ├── test_harmony.py
│ ├── test_mockup.py
│ └── test_project_io.py # si se implementan tests de IO
├── main.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md

Instalación

Clonar o descargar el repositorio:

git clone <URL_DEL_REPOSITORIO>
cd Divergesia

Crear y activar entorno virtual:

python3 -m venv .venv
source .venv/bin/activate # Linux/Mac

# Windows (PowerShell): .venv\Scripts\Activate.ps1

Instalar dependencias:

pip install -r requirements.txt

Ejecución

Ejecutar la aplicación:

python main.py

Se abrirá la ventana principal donde podrás cargar imágenes, extraer y ajustar paletas.

Ejecutar tests:

pytest -q

Asegurarse de que todos los tests pasen antes de desplegar o integrar cambios.

Uso de la aplicación

Cargar imagen: Abrir una imagen (PNG, JPEG, BMP). La vista mostrará la imagen escalada.

Extraer colores: Automáticamente extrae la paleta dominante de 5 colores por defecto.

Ver swatches: Los cuadrados de colores representan los colores extraídos.

Mockup: Bloques visuales de la paleta para previsualización.

Ajuste HSV: En el panel derecho, desplaza matiz, saturación o valor para modificar la paleta en tiempo real.

Revertir: Tras ajustes, pulsa “Revertir a paleta original” para volver a la paleta extraída o cargada.

Generar armonía: Botones para crear paleta complementaria, análoga, triada, tétrada o monocromática manteniendo mismo número de colores.

Guardar paleta: Exporta a JSON, CSS o CSV. JSON incluye metadatos para recargar.

Abrir paleta: Carga un archivo JSON previamente guardado; muestra la paleta sin modificar la imagen original.

Historial de paletas: Las paletas cargadas/extractadas aparecen en la lista de sesión; seleccionar una restaura sus colores.

Desarrollo y pruebas

Agregar nuevas funcionalidades: Sigue la estructura de paquetes:

Lógica pura en logic/.

Modelos y serialización en data/.

UI en ui/.

Trabajos en segundo plano en async_tasks/.

Escribir tests: Añade pruebas en tests/ con prefijo test\_\*.py. Usa pytest para asegurar calidad.

Configuración pytest: En pytest.ini, definiendo testpaths = tests. En conftest.py, configura QT_QPA_PLATFORM=offscreen para entornos sin GUI.

Dependencias: Mantener actualizadas en requirements.txt. Versiona dependencias críticas para reproducibilidad.

Control de versiones: Realiza commits frecuentes y descriptivos. Usa ramas para nuevas features y revisiones de código.

Personalización

Número de colores: Actualmente se extraen 5 colores por defecto. Para cambiar, ajusta en ClusteringWorker o añade opción en UI.

Tamaño de mockup o vista de imagen: Modifica valores de maximumSize o parámetros de crear_mockup_ui.

Ajustes de armonía: Los ángulos o porcentajes por defecto están en logic/harmony.py; edítalos o expón controles en UI para configurarlos.

Estilo de la interfaz: Añade estilos Qt o recursos (archivos QSS) en ui/resources/ para personalizar apariencia.

Soporte de más formatos: Extiende data/project_io.py para CSV/CSS en carga, o importación desde otros formatos.
