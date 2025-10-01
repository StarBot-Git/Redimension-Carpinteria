from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QSizePolicy

from app.config import settings
from app.ui.panels.top_bar import TopBar
from app.ui.panels.selection_panel import SelectionPanel
from .views import MetricsEditorView
from app.controllers.panel_selection_controller import SelectionPanelController
from app.services.repository_DB import RepositoryDB


class MainWindow(QMainWindow):
    """
    Shell de la aplicación: por ahora solo un contenedor vacío.
    Más adelante aquí montamos:
      - TopBar (chrome)
      - Sidebar fijo (panel de selección)
      - Área de contenido (QStackedWidget con vistas dinámicas)
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(settings.APP_NAME)
        self.resize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)

        self.inventor = None

        # ======== Layout principal ========

        central = QWidget(self) # Contenedor principal
        central.setObjectName("central") 

        root = QVBoxLayout(central) # Contenedor raiz
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # ======== Top Bar ========

        self.topbar = TopBar(self) # Barra superior | .py externo
        self.topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.topbar.setFixedHeight(80)
        root.addWidget(self.topbar)

        # ========= Separador horizontal  | Decorativo ========

        divider = QFrame(self)
        divider.setObjectName("TopDivider")
        divider.setFrameShape(QFrame.HLine)
        root.addWidget(divider)

        # ======== Contenedor | Sidebar + Content ========
            # - Sidebar (panel de selección)
            # - Separador vertical (decorativo)
            # - Content (vista dinámica)

        row = QHBoxLayout()
        row.setContentsMargins(16,16,16,16)
        row.setSpacing(16)
        root.addLayout(row)

        # ========= Sidebar (panel de selección) ========

        self.sidebar = SelectionPanel(self) # Panel Lateral | .py externo
        self.sidebar.setFixedWidth(285)

        self.DB = RepositoryDB() # Instancia de conexion a base de datos
        self._SelectionPanelController = SelectionPanelController(self, self.DB) # Controlador del panel de selección
        self._SelectionPanelController.Start_SP() # Cargar datos iniciales proveniente de la base de datos

        row.addWidget(self.sidebar, 0, Qt.AlignTop)

        # ========= Separador vertical | Decorativo ========

        vsep = QFrame(self); vsep.setObjectName("SideDivider"); vsep.setFrameShape(QFrame.VLine)
        row.addWidget(vsep)

        # ========= Contenedor formulario ========

        self.content = QWidget(self)
        self.content.setObjectName("ContentArea")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(8)

        # ========= Vista de formulario (MetricsEditorView) ========

        self.metrics_view = MetricsEditorView(self.content)
        content_layout.addWidget(self.metrics_view, 1)

        row.addWidget(self.content, 1)

        # ======== Inicialización | Widget central ========

        self.setCentralWidget(central)

    def closeEvent(self, event) -> None:
        try:
            if hasattr(self.metrics_view, "inventor") and self.metrics_view.inventor:
                # cierra docs primero para evitar diálogos
                for doc in list(self.metrics_view.inventor.Documents):
                    try:
                        doc.Close(True)  # True = sin prompts
                    except Exception:
                        pass
                # cierra Inventor
                self.metrics_view.inventor.Quit()
                print("✅ Inventor cerrado desde MainWindow")
        except Exception as e:
            print(f"⚠ No se pudo cerrar Inventor: {e}")
        finally:
            event.accept()