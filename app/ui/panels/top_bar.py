from PySide6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from app.config import settings

from app.controllers.topbar_controller import TopBarController

class TopBar(QFrame):
    def __init__(self, parent:QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("TopBar")

        # ======== Layout principal =========

        aux_layout = QHBoxLayout(self)
        aux_layout.setContentsMargins(24, 12, 24, 12)
        aux_layout.setSpacing(12)

        # ======== Titulo de la barra =========

        self._title = QLabel(settings.APP_NAME, self)
        self._title.setObjectName("TopBarTitle")

        aux_layout.addWidget(self._title, 0, Qt.AlignVCenter)

        # ========= Creacion de Breadcrumbs ========

        self._crumbs_container = QWidget(self)
        self._crumbs_container.setObjectName("Breadcrumbs")

        self._crumbs_Layout = QHBoxLayout(self._crumbs_container)
        self._crumbs_Layout.setContentsMargins(0, 0, 0, 0)
        self._crumbs_Layout.setSpacing(8)

        aux_layout.addWidget(self._crumbs_container, 0, Qt.AlignVCenter)

        # ========= Botones | Cotizado, Seccionado e Informacion =========

        self.button_quote = QPushButton("Cotizar")
        self.button_quote.clicked.connect(TopBarController.cotizar)
        self.set_TopBar_Button_Style(self.button_quote, icon_path=r"assets\icons\quote.svg")

        self.button_CutSaw = QPushButton("Seccionar")
        #self.button_CutSaw.clicked.connect()
        self.set_TopBar_Button_Style(self.button_CutSaw, icon_path=r"assets\icons\saw.svg")

        self.button_Information = QPushButton("Informacion")
        #self.button_Information.clicked.connect()
        self.set_TopBar_Button_Style(self.button_Information, icon_path=r"assets\icons\info.svg")

        aux_layout.addStretch(1)
        aux_layout.addWidget(self.button_quote)
        aux_layout.addWidget(self.button_CutSaw)
        aux_layout.addWidget(self.button_Information)

        # ========= Inicializar | Breadcrumbs ============

        self.set_breadcrumbs(["Products", "Type Model", "Select Model"])

        # =========================================

    def set_breadcrumbs(self, crumbs: list[str]) -> None:

        # ========= Eliminar | Breadcrumbs previos =========
        while self._crumbs_Layout.count():
            crumb_Name = self._crumbs_Layout.takeAt(0).widget()
            if crumb_Name:
                crumb_Name.deleteLater()

        # ========= Actualizacion | Breadcrumbs nuevos =========
        for i, crumb in enumerate(crumbs):
            crumb_Name = QLabel(crumb, self._crumbs_container)
            crumb_Name.setObjectName("Crumb")
            self._crumbs_Layout.addWidget(crumb_Name)

            if i < len(crumbs) - 1:
                separator = QLabel(">", self._crumbs_container)
                separator.setObjectName("CrumbSeparator")
                self._crumbs_Layout.addWidget(separator)

    def set_TopBar_Button_Style(self, button:QPushButton, icon_path:str = ""):
        # === Estilo base | Button ===
        button.setObjectName("TopBar_Button")
        button.setEnabled(False)
        #button.setMinimumHeight(18)
        button.setCursor(Qt.PointingHandCursor)

        if icon_path:
            button.setIcon(QIcon(icon_path)) 
            button.setIconSize(QSize(16, 16))  