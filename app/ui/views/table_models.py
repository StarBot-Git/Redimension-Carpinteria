from PySide6.QtGui import QStandardItemModel, QStandardItem


class BaseTableModel(QStandardItemModel):
    """Modelo base con headers y método para setear filas."""
    def __init__(self, headers, parent=None):
        super().__init__(0, len(headers), parent)
        self.HEADERS = headers
        self.setHorizontalHeaderLabels(self.HEADERS)

    def set_rows(self, rows: list[dict]):
        """Recibe lista de dicts con keys iguales a HEADERS."""
        self.removeRows(0, self.rowCount())
        for r in rows:
            items = [QStandardItem(str(r.get(h, ""))) for h in self.HEADERS]
            self.appendRow(items)


class MetricsModel(BaseTableModel):
    def __init__(self, parent=None):
        headers = ["Parametro", "Valor", "Unidad"]
        super().__init__(headers, parent)


class PropertiesModel(BaseTableModel):
    def __init__(self, parent=None):
        headers = ["Pieza", "Material", "Textura", "Color", "Proveedor", "Acabado"]
        super().__init__(headers, parent)
