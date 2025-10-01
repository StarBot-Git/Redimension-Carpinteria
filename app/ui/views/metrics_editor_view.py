from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


class MetricsEditorView(QFrame):
    HEADERS = ["Parametro", "Pieza", "Valor", "Unidad"]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("MetricsCard")

        # ======== Elemento raiz ========

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # ======== Titulo ========

        self.title = QLabel(f"Editor de metricas")
        self.title.setObjectName("MetricsCardTitle")
        root.addWidget(self.title)

        # ======== Contenedor | buscador ========

        search_row = QHBoxLayout()
        search_row.setSpacing(8)

        # ======== Barra buscadora de metricas ========

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar metrica...")
        self.search.setObjectName("SearchField")
        search_row.addWidget(self.search)

        root.addLayout(search_row)

        # ======== Botones | Funcionalidades varias ========

        actions = QHBoxLayout()
        self.btn_Model   = QPushButton("Ver Modelo")
        self.btn_Model.setEnabled(False)
        self.btn_Model.clicked.connect(self.on_view_model)

        self.btn_Drawings = QPushButton("Planos")
        self.btn_Drawings.setEnabled(False) 
        self.btn_Drawings.clicked.connect(self.on_view_drawings)

        self.btn_Import= QPushButton("⤓ Despiece CSV")
        self.btn_Import.setEnabled(False)
        self.btn_Import.clicked.connect(self.on_import_csv)

        self.btn_Save= QPushButton("Guardar Cambios")
        self.btn_Save.setEnabled(False)
        self.btn_Save.clicked.connect(self.on_save_changes)

        actions.addWidget(self.btn_Model)
        actions.addWidget(self.btn_Drawings)
        actions.addWidget(self.btn_Import)
        actions.addStretch(1)
        actions.addWidget(self.btn_Save)
        root.addLayout(actions)

        # ======== Tabla de metricas ========

        self.view = QTableView(self)
        self.view.setObjectName("MetricsTable")
        self.view.setAlternatingRowColors(True) # Alternar colores de filas
        self.view.setSelectionBehavior(QTableView.SelectRows) # Seleccionar filas completas
        self.view.setSortingEnabled(False) # Deshabilitar permisos de ordenamiento
        root.addWidget(self.view, 1)

        
        self.model = QStandardItemModel(0, len(self.HEADERS), self) # 0 filas, n columnas
        self.model.setHorizontalHeaderLabels(self.HEADERS) # Encabezados de columnas
        self.view.setModel(self.model)
        self.view.horizontalHeader().setStretchLastSection(True) # Ultima columna estirada
        self.view.verticalHeader().setVisible(False) # Ocultar encabezado vertical
        #self._populate_demo()  # 3 filas

    """
        set_model_name:

        Actualiza el título del MetricsEditorView con el nombre del modelo seleccionado.
    """

    def set_model_name(self, model_name: str):
        if model_name:
            self.title.setText(f"Editor de metricas - Modelo: {model_name}")
        else:
            self.title.setText("Editor de metricas")

    # ---------- Buttons ----------

    def on_view_model(self):
        print("Ver modelo")

    def on_view_drawings(self):
        print("Ver planos")

    def on_import_csv(self):
        print("Exportar despiece CSV")

    def on_save_changes(self):
        print("Guardar cambios")
    
    # ---------- Table Setup ----------

    def set_rows(self, rows: list[dict]):
        """
        rows: [{"Parametro": str, "Pieza": str, "Valor": any, "Unidad": str}, ...]
        """
        self.model.removeRows(0, self.model.rowCount())
        
        for r in rows:
            self._append_row(
                r.get("Parametro",""),
                r.get("Pieza",""),
                r.get("Valor",""),
                r.get("Unidad","mm"),
            )
        
        self.view.resizeColumnsToContents()

    # ---------- Interno ----------
    def _populate_demo(self):
        demo = [
            ("Height", "Pieza1", 800, "mm"),
            ("Width",  "Pieza2", 300, "mm"),
            ("Depth",  "Pieza3", 200, "mm"),
        ]
        for row in demo:
            self._append_row(*row)
        self.view.resizeColumnsToContents()

    def _append_row(self, param, piece, value, unit):
        items = [
            QStandardItem(str(param)),        # read-only
            QStandardItem(str(piece)),        # editable
            QStandardItem(str(value)),        # editable
            QStandardItem(str(unit)),         # read-only
        ]
        # Marcar Min/Max como no editables
        for idx in (0, 1, 3):
            items[idx].setEditable(False)
        self.model.appendRow(items)