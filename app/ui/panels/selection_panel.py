from PySide6.QtWidgets import QFrame, QLabel, QComboBox, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class SelectionPanel(QWidget):
    """
    Panel lateral fijo para selección de opciones.
    Por ahora solo un placeholder vacío.
    Más adelante aquí montamos:
      - Lista de presets (QListWidget)
      - Filtros y opciones (QGroupBox con varios controles)
      - Botones de acción (QPushButton)
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("SelectionPanel")
        self.setAttribute(Qt.WA_StyledBackground, True) 

        wrap = QVBoxLayout(self)
        wrap.setContentsMargins(16, 16, 16, 16)
        wrap.setSpacing(14)

        title = QLabel("Panel de selección")
        title.setObjectName("SelectionPanelTitle")
        wrap.addWidget(title)

        self._model_Type = self._field(wrap, "Tipo de modelo:", ["Tipo de modelo..."])
        self._model = self._field(wrap, "Modelo:", ["Modelo..."])
        self._material = self._field(wrap, "Material:", ["Material..."])
        self._edge = self._field(wrap, "Tipo de canto:", ["Tipo de canto..."])

        wrap.setSpacing(20)

        wrap.addStretch(1)  # empuja todo hacia arriba

    def _field(self, parent_layout: QVBoxLayout, label_text: str, items: list[str]) -> QComboBox:
        _label = QLabel(label_text)
        _label.setObjectName("SPLabel")
        parent_layout.addWidget(_label)

        temp_CBox = QComboBox(self)
        temp_CBox.setObjectName("SPCombo")
        temp_CBox.addItems(items)
        parent_layout.addWidget(temp_CBox)

        return temp_CBox