from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QSizePolicy

from app.config import settings
from app.ui.panels.top_bar import TopBar
from app.ui.panels.selection_panel import SelectionPanel
from .views import MetricsEditorView


class MainWindow(QMainWindow):
    """
    Shell de la aplicación: por ahora solo un contenedor vacío.
    Más adelante aquí montamos:
      - TopBar (chrome)
      - Sidebar fijo (panel de selección)
      - Área de contenido (QStackedWidget con vistas dinámicas)
      - StatusBar
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(settings.APP_NAME)
        self.resize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)

        central = QWidget(self); central.setObjectName("central")
        root = QVBoxLayout(central); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # TopBar
        self.topbar = TopBar(self)
        self.topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.topbar.setFixedHeight(60)
        root.addWidget(self.topbar)
        divider = QFrame(self); divider.setObjectName("TopDivider"); divider.setFrameShape(QFrame.HLine)
        root.addWidget(divider)

        # --- Row: Sidebar (fixed) + Content (expand) ---
        row = QHBoxLayout(); row.setContentsMargins(16,16,16,16); row.setSpacing(16)
        root.addLayout(row)

        self.sidebar = SelectionPanel(self)
        self.sidebar.setFixedWidth(285)  # ancho del panel

        self._models_by_type = {
            "Cocina": ["CL-800", "CL-1200", "CL-1600"],
            "Baño": ["BN-600", "BN-800"],
            "Oficina": ["OF-1200", "OF-1600", "OF-2XX2"],
        }
        self._materials = ["MDF 15 mm", "MDF 18 mm", "Melamine 15 mm", "Plywood 18 mm"]
        self._edges     = ["ABS 0.45 mm", "PVC 1.0 mm", "PVC 2.0 mm"]

        # Poblado inicial
        self._seed_options()

        # Conexiones (cuando el usuario cambia)
        self.sidebar._model_Type.currentTextChanged.connect(self.on_model_type_changed)
        self.sidebar._model.currentTextChanged.connect(self.update_breadcrumbs)
        self.sidebar._material.currentTextChanged.connect(self.update_breadcrumbs)
        self.sidebar._edge.currentTextChanged.connect(self.update_breadcrumbs)
        self.update_breadcrumbs()

        row.addWidget(self.sidebar, 0, Qt.AlignTop)

        # separador vertical sutil (opcional)
        vsep = QFrame(self); vsep.setObjectName("SideDivider"); vsep.setFrameShape(QFrame.VLine)
        row.addWidget(vsep)

        self.content = QWidget(self)
        self.content.setObjectName("ContentArea")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(8)

        # ---- Añadir la tarjeta del editor
        self.metrics_view = MetricsEditorView(self.content)
        content_layout.addWidget(self.metrics_view, 1)

        row.addWidget(self.content, 1)

        self.setCentralWidget(central)

    def _set_items(self, combo, items):
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)
        combo.blockSignals(False)

    def _seed_options(self):
        sp = self.sidebar
        self._set_items(sp._model_Type, ["Select model type"] + list(self._models_by_type.keys()))
        self._set_items(sp._model,      ["Select model"])
        self._set_items(sp._material,   ["Select material"] + self._materials)
        self._set_items(sp._edge,       ["Select edge band"] + self._edges)

    def on_model_type_changed(self, text: str):
        if not text or text.startswith("Select"):
            self._set_items(self.sidebar._model, ["Select model"])
        else:
            models = self._models_by_type.get(text, [])
            self._set_items(self.sidebar._model, ["Select model"] + models)
        self.update_breadcrumbs()

    def _clean_piece(self, s: str, prefix: str) -> str:
        if not s or s.startswith(prefix):
            return ""
        return s

    def update_breadcrumbs(self):
        # Products > <Model Type> > <Model>
        t = self._clean_piece(self.sidebar._model_Type.currentText(), "Select")
        m = self._clean_piece(self.sidebar._model.currentText(), "Select")

        parts = ["Products"]
        if t: parts.append(t)
        if m: parts.append(m)
        self.topbar.set_breadcrumbs(parts)


