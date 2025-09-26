from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


class MetricsEditorView(QFrame):
    """Tarjeta del editor de métricas (demo 3×5)."""
    HEADERS = ["Parameter", "Value", "Unit", "Min", "Max"]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("MetricsCard")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Título
        title = QLabel("Metrics Editor")
        title.setObjectName("MetricsCardTitle")
        root.addWidget(title)

        search_row = QHBoxLayout()
        search_row.setSpacing(8)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search metric…")
        self.search.setObjectName("SearchField")
        search_row.addWidget(self.search)
        root.addLayout(search_row)

        # Fila: acciones (solo visual por ahora)
        actions = QHBoxLayout()
        self.btn_add   = QPushButton("Add metric")
        self.btn_bulk  = QPushButton("Bulk Edit")
        self.btn_import= QPushButton("Import CSV")
        actions.addWidget(self.btn_add)
        actions.addWidget(self.btn_bulk)
        actions.addWidget(self.btn_import)
        actions.addStretch(1)
        root.addLayout(actions)

        # Tabla
        self.view = QTableView(self)
        self.view.setObjectName("MetricsTable")
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setSortingEnabled(False)
        root.addWidget(self.view, 1)

        # Modelo
        self.model = QStandardItemModel(0, len(self.HEADERS), self)
        self.model.setHorizontalHeaderLabels(self.HEADERS)
        self.view.setModel(self.model)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.verticalHeader().setVisible(False)
        self._populate_demo()  # 3 filas

    def set_rows(self, rows: list[dict]):
        """
        rows: [{"param": str, "value": any, "unit": str, "min": num, "max": num}, ...]
        """
        self.model.removeRows(0, self.model.rowCount())
        for r in rows:
            self._append_row(
                r.get("param",""),
                r.get("value",""),
                r.get("unit","mm"),
                r.get("min",""),
                r.get("max",""),
            )
        self.view.resizeColumnsToContents()

    # ---------- Interno ----------
    def _populate_demo(self):
        demo = [
            ("Height", 1200, "mm", 800, 2400),
            ("Width",   800, "mm", 300, 2000),
            ("Depth",   400, "mm", 200,  600),
        ]
        for row in demo:
            self._append_row(*row)
        self.view.resizeColumnsToContents()

    def _append_row(self, param, value, unit, vmin, vmax):
        items = [
            QStandardItem(str(param)),        # editable
            QStandardItem(str(value)),        # editable
            QStandardItem(str(unit)),         # editable
            QStandardItem(str(vmin)),         # read-only
            QStandardItem(str(vmax)),         # read-only
        ]
        # Marcar Min/Max como no editables
        for idx in (3, 4):
            items[idx].setEditable(False)
        self.model.appendRow(items)