from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

# ====== Librerias propias ======

from app.ui.panels.top_bar import TopBar
from app.ui.panels.selection_panel import SelectionPanel
from app.ui.views import MetricsEditorView
from app.controllers.panel_selection_controller import SelectionPanelController
from app.services.repository_DB import RepositoryDB
from app.config import settings

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # ======== Configuracion inicial ========

        self.setWindowTitle(settings.APP_NAME) # Nombre de la aplicacion
        self.resize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT) # Tamaño inicial
        self.setWindowIcon(QIcon(settings.LOGO_DIR)) # Logo All Star | Barra de la App

        self.inventor = None # Inventor | Inicialmente vacio
        self.DB = RepositoryDB() # Base de datos | Conexion Inicial

        # ======== Layout principal ========

        central = QWidget(self) # Contenedor principal
        central.setObjectName("central")

        root = QVBoxLayout(central) # Contenedor raiz
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # ======== Top Bar ========

        self.topbar = TopBar(self) # Barra superior | .py externo
        self.topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # (Ancho, Alto)
        self.topbar.setFixedHeight(50)

        root.addWidget(self.topbar)

        # ========= Separador horizontal  | Decorativo ========

        divider = QFrame(self)
        divider.setObjectName("TopDivider")
        divider.setFrameShape(QFrame.HLine)

        root.addWidget(divider)

        # ======== Subcontenedor | Sidebar + Content/Table ========
            # - Sidebar (panel de selección)
            # - Separador vertical (decorativo)
            # - Content/Table (vista dinámica)

        dynamism_container = QHBoxLayout()
        dynamism_container.setContentsMargins(16,16,16,16)
        dynamism_container.setSpacing(16)
        
        root.addLayout(dynamism_container)

        # ========= Sidebar (panel de selección) ========

        self.sidebar = SelectionPanel(self) # Panel Lateral | .py externo
        self.sidebar.setFixedWidth(285)

        self._SelectionPanelController = SelectionPanelController(self, self.DB) # Controlador del panel de selección
        self._SelectionPanelController.Start_SP() # Cargar datos iniciales proveniente de la base de datos

        dynamism_container.addWidget(self.sidebar, 0, Qt.AlignTop)

        # ========= Separador vertical | Decorativo ========

        vsep = QFrame(self); vsep.setObjectName("SideDivider"); vsep.setFrameShape(QFrame.VLine)
        dynamism_container.addWidget(vsep)

        # ========= Contenedor de la tabla ========

        self.content = QWidget(self)
        self.content.setObjectName("ContentArea")

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(8)

        # ========= Vista de Tabla (MetricsEditorView) ========

        self.metrics_view = MetricsEditorView(self.content) # Tabla de metricas y propiedades | .py externo
        content_layout.addWidget(self.metrics_view, 1)

        dynamism_container.addWidget(self.content, 1)

        # ======== Inicialización | Widget central ========
        self.setCentralWidget(central)

    """
        closeEvent():

        Funcion que se ejecuta al cerrar la ventana principal. Aquí se maneja el cierre de Inventor si está abierto.
    """
    def closeEvent(self, event) -> None:
        try:
            # === Verificar y cerrar Inventor si está abierto ===
            if hasattr(self.metrics_view, "inventor") and self.metrics_view.inventor:

                # === cierra todos los documentos abiertos sin guardar ===
                for doc in list(self.metrics_view.inventor.Documents):
                    try:
                        doc.Close(True) # Sin prompts
                    except Exception:
                        pass
                
                # === cierra Inventor ===
                self.metrics_view.inventor.Quit()
                print("✅ Inventor cerrado desde MainWindow")

            try:
                if hasattr(self, "DB") and self.DB:
                    self.DB.close()
                    print("✅ DB cerrada")
            except Exception as e:
                print(f"⚠ No se pudo cerrar la base de datos: {e}")

        except Exception as e:
            print(f"⚠ No se pudo cerrar Inventor: {e}")
        finally:
            event.accept()