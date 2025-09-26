from PySide6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from app.config import settings

class TopBar(QFrame):
    def __init__(self, parent:QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("TopBar")

        # ======== Titulo y Objeto =========

        self._title = QLabel(settings.APP_NAME, self)
        self._title.setObjectName("TopBarTitle")

        # ========= Creacion de Breadcrumbs ========

        self._crumbs_container = QWidget(self)
        self._crumbs_container.setObjectName("Breadcrumbs")
        self._crumbs_Layout = QHBoxLayout(self._crumbs_container)
        self._crumbs_Layout.setContentsMargins(0, 0, 0, 0)
        self._crumbs_Layout.setSpacing(8)

        # ========= Layout horizontal ============
        aux_layout = QHBoxLayout(self)
        aux_layout.setContentsMargins(24, 12, 24, 12)
        aux_layout.setSpacing(12)
        aux_layout.addWidget(self._title, 0, Qt.AlignVCenter)
        aux_layout.addWidget(self._crumbs_container, 0, Qt.AlignVCenter)
        aux_layout.addStretch(1)

        self.set_breadcrumbs(["Products", "Closet", "Select Model"])

    def set_breadcrumbs(self, crumbs: list[str]) -> None:

        while self._crumbs_Layout.count():
            crumb_Name = self._crumbs_Layout.takeAt(0).widget()
            if crumb_Name:
                crumb_Name.deleteLater()

        for i, crumb in enumerate(crumbs):
            crumb_Name = QLabel(crumb, self._crumbs_container)
            crumb_Name.setObjectName("Crumb")
            self._crumbs_Layout.addWidget(crumb_Name)

            if i < len(crumbs) - 1:
                separator = QLabel(">", self._crumbs_container)
                separator.setObjectName("CrumbSeparator")
                self._crumbs_Layout.addWidget(separator)
