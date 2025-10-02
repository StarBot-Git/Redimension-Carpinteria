import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

"""
    apply_stylesheet():

    Carga la hoja de estilos desde el archivo main.qss y la aplica a la app.
"""
def apply_stylesheet(app: QApplication) -> None:

    # === Cargar hoja de estilos | main.qss ===
    style_path = Path(__file__).parent / "assets" / "styles" / "main.qss"

    if style_path.exists():
        # === Aplicar hoja de estilos ===
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

def main() -> int:
    app = QApplication(sys.argv)

    apply_stylesheet(app)

    window = MainWindow()
    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())