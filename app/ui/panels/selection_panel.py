from PySide6.QtWidgets import QFrame, QLabel, QComboBox, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

# ====== Librerias propias ======

from app.ui.widgets.loadingBar_widget import LoadingWidget

class SelectionPanel(QWidget):
  """
    class SelectionPanel():
      - Titulo
      - Linea divisora
      - Combo Boxes
      - Loading Widget
  """
  def __init__(self, parent: QWidget | None = None) -> None:
      super().__init__(parent)
      self.setObjectName("SelectionPanel")
      self.setAttribute(Qt.WA_StyledBackground, True)

      # ========= Contenedor | Layout Principal =========

      wrap = QVBoxLayout(self)
      wrap.setContentsMargins(16, 16, 16, 16)
      wrap.setSpacing(14)

      # ========= Título =========

      title = QLabel("Panel de selección")
      title.setObjectName("SelectionPanelTitle")

      wrap.addWidget(title)

      # ========= Separador horizontal | Decorativo =========

      divider = QFrame(self)
      divider.setObjectName("TopDivider")
      divider.setFrameShape(QFrame.HLine)

      wrap.addWidget(divider)

      # ========= ComboBoxes =========

      cb_container = QVBoxLayout()
      cb_container.setContentsMargins(0,0,0,0)
      cb_container.setSpacing(14)

      self._project = self._field(cb_container, "Proyecto:", ["Seleccione un proyecto..."])
      self._model_Type = self._field(cb_container, "Tipo de modelo:", ["Tipo de modelo..."])
      self._model = self._field(cb_container, "Modelo:", ["Modelo..."])

      # divider = QFrame(self)
      # divider.setObjectName("TopDivider")
      # divider.setFrameShape(QFrame.HLine)
      # wrap.addWidget(divider)

      self._material = self._field(cb_container, "Material:", ["Material..."])
      self._edge = self._field(cb_container, "Tipo de canto:", ["Tipo de canto..."])

      wrap.addLayout(cb_container)
      wrap.setSpacing(20)
      wrap.addStretch(1)  

      # ========= Loading widget | Diseño propio =========

      self.loading = LoadingWidget() # Barra de carga | .py externo
      self.loading.setVisible(False)

      wrap.addWidget(self.loading)

      # ==================================================


  """
    _field():
      Metodo que crea etiqueta y elementos de los Combo Box.
  """
  def _field(self, parent_layout: QVBoxLayout, label_text: str, items: list[str]) -> QComboBox:
      
      # ========= Etiqueta | ComboBox =========
      _label = QLabel(label_text)
      _label.setObjectName("SPLabel")
      parent_layout.addWidget(_label)

      # ========= Objeto | ComboBox =========
      temp_CBox = QComboBox(self)
      temp_CBox.setObjectName("SPCombo")
      temp_CBox.addItems(items)
      parent_layout.addWidget(temp_CBox)

      return temp_CBox