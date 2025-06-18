
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    # Instanciar la ventana principal
    window = MainWindow()
    window.show()
    # Ejecutar el bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
